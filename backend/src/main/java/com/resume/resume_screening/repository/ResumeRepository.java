package com.resume.resume_screening.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.resume.resume_screening.model.Resume;

public interface ResumeRepository extends JpaRepository<Resume, Long> {

}