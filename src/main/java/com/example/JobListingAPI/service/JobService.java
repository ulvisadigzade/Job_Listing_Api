package com.example.JobListingAPI.service;

import com.example.JobListingAPI.DTO.JobRequestDTO;
import com.example.JobListingAPI.DTO.JobResponseDTO;
import com.example.JobListingAPI.mapper.JobMapper;
import com.example.JobListingAPI.model.Job;
import com.example.JobListingAPI.repository.JobRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.hateoas.PagedModel;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;


@Service
@RequiredArgsConstructor
public class JobService {
    private final JobRepository jobRepository;
    private final JobMapper jobMapper;

    // get all jobs (with pagination)
    public PagedModel<JobResponseDTO> getJobs(int page){
        Pageable pageable = PageRequest.of(page,10);
        Page<Job> jobs = jobRepository.findAll(pageable);
        Page<JobResponseDTO> dtoPage = jobs.map(jobMapper::toResponse);
        return PagedModel.of(
                dtoPage.getContent(),
                new PagedModel.PageMetadata(
                        dtoPage.getSize(),
                        dtoPage.getNumber(),
                        dtoPage.getTotalElements(),
                        dtoPage.getTotalPages()
                )
        );
    }

    // get job by id
    public JobResponseDTO getJob(Long id){
        Job job = jobRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Pg not found"));
        return jobMapper.toResponse(job);
    }

    // save scraped job
    public void saveJob(JobRequestDTO jobRequestDTO){
        Job job = jobMapper.toEntity(jobRequestDTO);
        System.out.println(job);
        jobRepository.save(job);
    }

    // get last date
    public LocalDateTime getLastTime(){
        List<Job> jobs = jobRepository.findAll();
        if(jobs.isEmpty())throw new RuntimeException("exception");
        return jobs.stream()
                .map(Job::getDatePosed)
                .max(LocalDateTime::compareTo)
                .get();
    }
}
