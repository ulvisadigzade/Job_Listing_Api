package com.example.JobListingAPI.DTO;


import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

import java.time.LocalDateTime;


@AllArgsConstructor
@Getter
@Builder
@ToString
public class JobResponseDTO {
    private Long id;
    private String jobTitle;
    private String companyName;
    private String location;
    private String jobType;
    private String jobDescription;
    private String experienceLevel;
    private String educationLevel;
    private String industry;
    private LocalDateTime datePosted;
    private String howToApply;
    private String source;
}