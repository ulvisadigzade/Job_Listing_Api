package com.example.JobListingAPI.controller;


import com.example.JobListingAPI.DTO.JobRequestDTO;
import com.example.JobListingAPI.DTO.JobResponseDTO;
import com.example.JobListingAPI.model.Job;
import com.example.JobListingAPI.service.JobService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@RestController
@RequiredArgsConstructor
@RequestMapping("/scrape")
public class ScraperController {
    private final JobService jobService;

    //Get lates date for checking in scraper
    @GetMapping("/last")
    @ResponseStatus(HttpStatus.OK)
    public LocalDateTime getLastTime(){
        return jobService.getLastTime();
    }

    //Post scraped jobs
    @PostMapping("/jobs")
    @ResponseStatus(HttpStatus.CREATED)
    public void saveJob(@RequestBody JobRequestDTO jobRequestDTO){
        jobService.saveJob(jobRequestDTO);
    }


}
