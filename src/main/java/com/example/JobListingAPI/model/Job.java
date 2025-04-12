package com.example.JobListingAPI.model;


import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;


@Entity
@Table(name = "jobs")
@Getter @Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString
@Builder
public class Job {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String jobTitle;
    private String companyName;
    private String location;
    private String jobType;
    @Column(columnDefinition = "TEXT")
    private String jobDescription;
    private String experienceLevel;
    private String educationLevel;
    private String industry;
    private LocalDateTime datePosed;
    private String howToApply;
    private String source;
}
