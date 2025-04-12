package com.example.JobListingAPI.mapper;


import com.example.JobListingAPI.DTO.JobRequestDTO;
import com.example.JobListingAPI.DTO.JobResponseDTO;
import com.example.JobListingAPI.model.Job;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;


@Component
public class JobMapper {

    public Job toEntity(JobRequestDTO request){
        String jobDateStr = request.getDatePosted();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm dd.MM.yyyy");
        LocalDateTime jobDate = LocalDateTime.parse(jobDateStr, formatter);

        return Job.builder()
                .jobTitle(request.getJobTitle())
                .companyName(request.getCompanyName())
                .location(request.getLocation())
                .jobType(request.getJobType())
                .jobDescription(request.getJobDescription())
                .experienceLevel(request.getExperienceLevel())
                .educationLevel(request.getEducationLevel())
                .industry(request.getIndustry())
                .datePosed(jobDate)
                .howToApply(request.getHowToApply())
                .source(request.getSource())
                .build();
    }

    public JobResponseDTO toResponse(Job job){

        return JobResponseDTO.builder()
                .id(job.getId())
                .jobTitle(job.getJobTitle())
                .companyName(job.getCompanyName())
                .location(job.getLocation())
                .jobType(job.getJobType())
                .jobDescription(job.getJobDescription())
                .experienceLevel(job.getExperienceLevel())
                .educationLevel(job.getEducationLevel())
                .industry(job.getIndustry())
                .datePosted(job.getDatePosed())
                .howToApply(job.getHowToApply())
                .source(job.getSource())
                .build();
    }
}
