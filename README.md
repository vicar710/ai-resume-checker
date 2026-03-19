# AI Resume Checker & LinkedIn Job Scraper

📺 Project Demonstration Video  
https://www.youtube.com/watch?v=xZho8_A3XHw

---

# Project Overview

This project implements a **Generative AI-powered Resume Checker and LinkedIn Job Scraper** designed to help job seekers optimize their resumes and discover relevant job opportunities automatically.

The system analyzes resumes using **Google Gemini (LLM)** to provide structured feedback such as ATS compatibility, strengths, weaknesses, and improvement suggestions. In addition, it integrates a **LinkedIn job scraper built with Selenium** to retrieve job listings directly from LinkedIn based on user queries.

Traditional resume evaluation is manual and subjective. This tool automates the process using AI to generate insights and recommendations instantly.

The application provides a **Streamlit-based interactive interface** where users can upload resumes, analyze their content, and explore LinkedIn job opportunities in a single workflow.

---

# Problem Statement

Job seekers often struggle with:

* Determining whether their resume will pass **Applicant Tracking Systems (ATS)**
* Identifying **strengths and weaknesses** in their resume
* Aligning their resume with **industry or FAANG-level standards**
* Finding relevant job listings efficiently

Manual resume evaluation is time-consuming and subjective.

This project addresses these challenges by:

* Automatically analyzing resumes using **Generative AI**
* Providing **ATS compatibility insights**
* Generating **resume improvement suggestions**
* Scraping **LinkedIn job listings** relevant to the user

---

# System Design and Architecture

## High-Level Architecture

```
Resume Upload (Streamlit UI)
        │
        ▼
PDF Text Extraction
        │
        ▼
Content Parsing
        │
        ▼
Gemini LLM Analysis
        │
        ▼
Resume Insights
(ATS Score, Strengths, Weaknesses, Summary)
        │
        ▼
LinkedIn Job Query
        │
        ▼
Selenium Web Scraper
        │
        ▼
Job Listings Output
```

---

# System Components

## 1. User Interface

* Built using **Streamlit**
* Allows users to upload resumes
* Displays AI-generated resume insights
* Provides LinkedIn job search interface

---

## 2. Resume Parser

* Extracts text from uploaded **PDF resumes**
* Processes raw resume content for analysis
* Converts resume text into structured input for the LLM

---

## 3. Gemini LLM Integration

The system uses **Google Gemini API** for intelligent resume analysis.

Gemini is responsible for:

* Generating professional resume summaries
* Identifying strengths and weaknesses
* Evaluating ATS compatibility
* Suggesting resume improvements
* Assessing alignment with FAANG-style hiring expectations

---

## 4. LinkedIn Job Scraper

The LinkedIn job search feature uses **Selenium automation**.

The scraper performs:

* Automated LinkedIn job search
* Job listing extraction
* Collection of job titles, companies, and links
* Display of relevant jobs inside the Streamlit app

This allows users to discover **relevant opportunities after optimizing their resumes**.

---

# Technical Approach

## Step 1: Resume Analysis

1. User uploads resume
2. Resume text extracted from PDF
3. Text passed to Gemini API
4. Gemini generates structured resume analysis

Generated insights include:

* Professional summary
* ATS compatibility insights
* Resume strengths
* Resume weaknesses
* Suggestions for improvement

---

## Step 2: LinkedIn Job Search

1. User enters job role or keyword
2. Selenium launches automated browser
3. LinkedIn job search executed
4. Job listings scraped
5. Results displayed in the Streamlit interface

---

# How Selenium is Used

Selenium is used to automate LinkedIn job searches.

### Key Operations

* Open LinkedIn job search page
* Enter search query
* Extract job listing elements
* Collect job titles and links

Example workflow:

```
User Job Query
        │
        ▼
Selenium Browser Automation
        │
        ▼
LinkedIn Job Search
        │
        ▼
Extract Job Listings
        │
        ▼
Display Results
```

---

# Project Structure

```
ai-resume-checker-linkedin-scraper/
│
├── app.py                # Streamlit application
├── resume_analyzer.py    # Gemini API integration
├── linkedin_scraper.py   # Selenium scraping logic
├── parser.py             # Resume text extraction
│
├── utils/                # Helper functions
│
├── requirements.txt      # Project dependencies
└── README.md             # Documentation
```

---

# Setup and Execution Instructions

## Step 1: Clone Repository

```
git clone https://github.com/AayushTripathi07/ai-resume-checker-linkedin-scraper.git
cd ai-resume-checker-linkedin-scraper
```

---

## Step 2: Install Dependencies

```
pip install -r requirements.txt
```

---

## Step 3: Add Gemini API Key

Create an environment variable for your Gemini API key:

```
export GEMINI_API_KEY="your_api_key_here"
```

---

## Step 4: Run Streamlit Application

```
streamlit run app.py
```

Application runs at:

```
http://localhost:8501
```

---

# Example Usage

### Resume Analysis

Upload a PDF resume and the system will generate:

* Professional summary
* ATS compatibility insights
* Strengths and weaknesses
* Resume improvement suggestions

---

### LinkedIn Job Search

Enter queries such as:

```
Data Analyst
Machine Learning Engineer
AI Engineer
Business Intelligence Analyst
```

The system retrieves LinkedIn job listings using Selenium.

---

# Key Features

* AI-powered resume analysis
* ATS compatibility checking
* Resume improvement suggestions
* LinkedIn job scraping using Selenium
* Generative AI insights using Gemini
* Interactive Streamlit interface

---

# Technical Stack

| Component | Technology |
|----------|-------------|
| Frontend | Streamlit |
| Backend | Python |
| LLM | Google Gemini API |
| Web Scraping | Selenium |
| Resume Parsing | Python PDF tools |
| AI Processing | NLP + LLM |

---

# Performance and Scalability

The system provides:

* Instant resume feedback using Gemini LLM
* Automated job search from LinkedIn
* Lightweight Streamlit interface
* Modular architecture for future extensions

The architecture can be extended to support:

* Multiple resume formats
* Job matching algorithms
* Cloud deployment

---

# Future Improvements

Possible extensions include:

* Resume-to-job matching engine
* ATS scoring visualization dashboard
* Multi-platform job scraping
* Automated resume tailoring
* RAG-based career assistant
* Deployment on cloud infrastructure

---

# Conclusion

This project demonstrates how **Generative AI and automation** can be combined to build intelligent career tools.

By integrating **Gemini for resume analysis** and **Selenium for LinkedIn job scraping**, the system helps users:

* Improve resume quality
* Understand ATS compatibility
* Discover relevant job opportunities

The project showcases a practical application of **LLMs, web scraping, and interactive AI systems** in the recruitment domain.

---

⭐ Developed by **Utsav and his team**
