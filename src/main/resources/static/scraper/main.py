from job_scraper import scrape
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import requests

    
app = FastAPI()


#install uvicorn


def send_data_to_spring():
    target_url = "http://localhost:8080/scrape/"

    last_time = requests.get(target_url+"last")
    print(last_time.text)


    job_datas = scrape(last_time.text)

    for job_data in job_datas:
        requests.post(target_url+"jobs",json=job_data)
        

# Run every 3 hours
scheduler = BackgroundScheduler()
scheduler.add_job(send_data_to_spring, 'interval', hours=1)
scheduler.start()

send_data_to_spring()


@app.get("/")
def root():
    return {"status": "Scheduled task is active!"}


