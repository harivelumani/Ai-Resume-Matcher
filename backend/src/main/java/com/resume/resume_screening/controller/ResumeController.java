package com.resume.resume_screening.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;

import org.springframework.core.io.ByteArrayResource;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

@RestController
@RequestMapping("/resume")
@CrossOrigin(origins = "*")
public class ResumeController {

    @PostMapping("/match")
    public Map<String,Object> match(
            @RequestParam("resume") MultipartFile resumeFile,
            @RequestParam("jd") String jdText){

        Map<String,Object> response = new HashMap<>();

        try{

            // Extract resume text (optional but good to keep)
            PDFTextStripper stripper = new PDFTextStripper();
            PDDocument resumeDoc = PDDocument.load(resumeFile.getInputStream());
            String resumeText = stripper.getText(resumeDoc);
            resumeDoc.close();

            // CALL PYTHON AI SERVICE
            RestTemplate restTemplate = new RestTemplate();

MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();

body.add("resume", new ByteArrayResource(resumeFile.getBytes()) {
    @Override
    public String getFilename() {
        return resumeFile.getOriginalFilename();
    }
});

body.add("jd", jdText);

HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.MULTIPART_FORM_DATA);

HttpEntity<MultiValueMap<String, Object>> requestEntity =
        new HttpEntity<>(body, headers);

ResponseEntity<Map> aiResponse =
        restTemplate.postForEntity(
                "http://localhost:8000/match",
                requestEntity,
                Map.class
        );

Double score = Double.valueOf(
        aiResponse.getBody().get("matchScore").toString()
);

            response.put("matchScore",score);

        }catch(Exception e){
            e.printStackTrace();
            response.put("error",e.getMessage());
        }

        return response;
    }
}
