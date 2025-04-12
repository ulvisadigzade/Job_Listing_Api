from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, List


BASE_URL = 'https://djinni.co'

DATE_FORMAT = "%H:%M %d.%m.%Y"
MINUTES_IN_3_MONTHS = 3 * 30 * 24 * 60

# Add these constants at the top
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0"
COOKIES = {
    "sessionid":".eJxVkMtuwyAQRf-FbRsHBkyMd63UZXdddYOGhx2nNkQYqy_l3zupWqndAXPu1Rw-mc9bquXd-hwi69nd8wO7ZZhyYv0nmwI94cBbdXAwdEKqIGMXPAyAUkUJSgdHvC8Ra7zCwKHdcbnjhyfR9pz3ijfSGK3hhi6cEzzMOK7UfrnQueSFUvtTduve5-WM6X3ncn5Z8LwLRg9-T4kxV1u2OVKqli3eMotbPdptjcV-r2i00BzYv4FD_xLTdRpOmMbc-Eyik2uuSPMzXZtH8p7vf9h_BUdcj5SOfjBu8MJ4CJ3W2Do1oDKyk4eWzBS0bec1lyiAPCWZdtFhUMJwCEIrKo0LTrNdpzFt51-FtWKp9nX6wBJsnZb45_NAP3HTg-oFNCCgFZpKUnz75VmftnmmjrwVfw3W0bpc2eULgUWPVg:1u2kZu:6knhKhf8IclHzRAiEGXfbiUszQAZPKhA3KVJIlm0PaM",
    "csrftoken": "BFqBZssTtMtHMYAQupPlMmbWEDyVsMDE"
}
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": BASE_URL,
}

def can_be_taken(date_str: str, last_time: Optional[str]) -> bool:
    # Current time in Ukraine (UTC+3)
    ukraine_time = datetime.now() - timedelta(hours=1)

    # Convert job date from string to datetime
    try:
        job_date = datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        return False

    # Check if job date is more than 3 months ago
    time_diff = (ukraine_time - job_date).total_seconds() / 60
    if time_diff > MINUTES_IN_3_MONTHS:
        return False

    # If no last_time provided, we can take this job
    if last_time is None:
        return True

    # Parse last_time from ISO format
    try:
        last_datetime = datetime.fromisoformat(last_time)
    except ValueError:
        return True  # If can't parse, assume we should take this job

    # Only take jobs newer than our last scraped job
    return job_date > last_datetime


def create_job_dict(
    job_title: str,
    company_name: str,
    location: str,
    job_type: str,
    job_description: str,
    experience_level: str,
    education_level: str,
    industry: str,
    date_posted: str,
    how_to_apply: str,
    source: str
) -> Dict[str, str]:
    """Create a standardized job dictionary."""
    return {
        "jobTitle": job_title,
        "companyName": company_name,
        "location": location,
        "jobType": job_type,
        "jobDescription": job_description,
        "experienceLevel": experience_level,
        "educationLevel": education_level,
        "industry": industry,
        "datePosted": date_posted,
        "howToApply": how_to_apply,
        "source": source
    }


def scrape_job(job_url: str, job_date: str) -> Optional[Dict[str, str]]:
    full_url = BASE_URL + job_url

    try:
        response = requests.get(
            full_url,
            headers=HEADERS,
            cookies=COOKIES,
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(response.text, 'lxml')

    # Check if job meets our criteria
    is_remote = "Full Remote" in soup.text
    location_tag = soup.find('span', class_='location-text')

    if not (
        (is_remote and ("Azerbaijan" in soup.text or "Worldwide" in soup.text))
        or "Relocation" in soup.text
    ):
        return None

    # Extract job details
    job_title = soup.find('h1').find('span').text.strip()
    company_name = soup.find('div', class_='col').text.strip()
    location = location_tag.text.strip() if location_tag else ""

    # Job description
    description_div = soup.find('div', ['mb-4', 'job-post__description'])
    job_description = description_div.get_text(strip=True) if description_div else ""

    # Experience level
    right_div = soup.find('div', ['col-lg-4', 'order-lg-1', 'order-0', 'mb-4', 'mb-lg-0'])
    experience_level = ""
    if right_div:
        for strong in right_div.find_all('strong'):
            if "experience" in strong.text.lower():
                experience_level = strong.text.strip()
                break

    # Industry/Domain
    industry = ""
    for div_col in soup.find_all('div', class_='col'):
        if 'Domain:' in div_col.text:
            industry = div_col.text.strip()[7:]  # Remove "Domain:"
            break

    # Format the date
    try:
        actual_date = datetime.strptime(job_date, DATE_FORMAT)
        date_posted = actual_date.strftime(DATE_FORMAT)
    except ValueError:
        date_posted = ""

    # Keywords
    keywords = ""

    # Source (external application URL)
    source = ""
    for url in soup.find_all('a'):
        if "http" in url.text:
            source = url['href']
            break

    return create_job_dict(
        job_title=job_title,
        company_name=company_name,
        location=location,
        job_type="",  # You might want to extract this
        job_description=job_description,
        experience_level=experience_level,
        education_level="",  # You might want to extract this
        industry=industry,
        date_posted=date_posted,
        how_to_apply=full_url,
        source=source
    )


def scrape(last_time: Optional[str] = None) -> List[Dict[str, str]]:
    jobs = []
    page = 1
    should_continue = True

    while should_continue:
        # Build URL for current page
        url = f"{BASE_URL}/jobs/?page={page}" if page > 1 else f"{BASE_URL}/jobs/"

        try:
            response = requests.get(
                url,
                headers=HEADERS,
                cookies=COOKIES,
                timeout=10
            )
            response.raise_for_status()

            # Stop if we're redirected to page 1 (no more pages)
            if page > 1 and response.url == f"{BASE_URL}/jobs/":
                break

            soup = BeautifulSoup(response.text, 'lxml')
            job_list = soup.find('ul', ['list-unstyled', 'list-jobs', 'mb-4'])
            if not job_list:
                break

            for job_item in job_list.find_all('li', class_='mb-4'):
                # Extract job date
                date_span = job_item.find('span', attrs={"title": True})
                if not date_span:
                    continue

                if can_be_taken(date_span['title'], last_time):
                    job_link = job_item.find('a', class_='job-item__title-link')
                    if job_link:
                        job_data = scrape_job(job_link['href'], date_span['title'])
                        if job_data:
                            jobs.append(job_data)
                else:
                    should_continue = False
                    break

            if page==2:
                break
            page += 1

        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
            
    return jobs