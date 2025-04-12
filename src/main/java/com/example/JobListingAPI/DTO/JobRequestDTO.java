package com.example.JobListingAPI.DTO;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;


@AllArgsConstructor
@Getter
@ToString
public class JobRequestDTO {
    private String jobTitle;
    private String companyName;
    private String location;
    private String jobType;
    private String jobDescription;
    private String experienceLevel;
    private String educationLevel;
    private String industry;
    private String datePosted;
    private String howToApply;
    private String source;
}