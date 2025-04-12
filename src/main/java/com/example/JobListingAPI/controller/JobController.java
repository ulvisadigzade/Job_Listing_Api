package com.example.JobListingAPI.controller;


import com.example.JobListingAPI.DTO.JobRequestDTO;
import com.example.JobListingAPI.DTO.JobResponseDTO;
import com.example.JobListingAPI.service.JobService;
import lombok.RequiredArgsConstructor;
import org.springframework.hateoas.PagedModel;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
public class JobController {
    private final JobService jobService;

    //Get all jobs (with pagination, /jobs?page=2) each page has 10 jobs
    @GetMapping("/jobs")
    @ResponseStatus(HttpStatus.OK)
    public PagedModel<JobResponseDTO> getJobs(@RequestParam(defaultValue = "0") int page){
        return jobService.getJobs(page);
    }

    //Get 1 job by it's id
    @GetMapping("/jobs/{id}")
    @ResponseStatus(HttpStatus.OK)
    public JobResponseDTO getJob(@PathVariable Long id){
        return jobService.getJob(id);
    }

}
