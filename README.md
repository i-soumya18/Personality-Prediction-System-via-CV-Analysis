# Personality Prediction System

## Project Overview

The Personality Prediction System is an AI-powered application designed to analyze resumes or textual data provided by candidates, predict their personality traits, and assist recruiters in making informed hiring decisions. This system utilizes various technologies and techniques, including machine learning, natural language processing (NLP), and a web interface to streamline the candidate evaluation process.

#Installation Guide
## copy this repo link and open on your IDE
## Create your Gemini Api key going through the link below.
>  https://makersuite.google.com/app/apikey
## Install the requirements
> pip install r- requirements.txt
## Run the app.py
> python app.py
## Enjoy -:)


## Technologies Used

- **Programming Languages**: Python (for backend), HTML, CSS, JavaScript (for web interface)
- **Libraries/Frameworks**: Flask (web development), Pandas (data handling), NLTK (NLP), Google GenerativeAI (AI interaction)
- **Tools**: PyPDF2, textract, docx (for text extraction from resumes)

## Implementation Details

### Resume Processing and Trait Assignment
- Extracts textual data from resumes using Python libraries such as PyPDF2, textract, and docx.
- Preprocesses the text by removing punctuation, tokenization, and lemmatization using NLTK.
- Assigns personality traits to candidates based on extracted skills and predefined associations from 'traits.txt'.

### Web Interface and User Interaction
- Implements a Flask-based web application to facilitate resume uploads and display analysis results.
- Renders HTML templates ('index.html' and 'result.html') for user interaction and displaying extracted details.

### AI Interaction for Trait Description
- Interacts with Google's GenerativeAI service to describe a candidate's personality based on assigned traits.
- Constructs queries to the AI model based on the assigned personality traits for trait descriptions.

### Data Management and History
- Stores extracted resume details in a CSV file ('extracted_details.csv') for historical reference.
- Offers functionalities to view history, export data, and clear history through specific endpoints in the web application.

## Objective and Use Cases

The primary objective of the Personality Prediction System is to streamline the candidate evaluation process for recruiters and employers. This system aids in making informed hiring decisions by providing insights into candidate personalities based on their resumes or textual data.

### Use Cases

- **Recruitment Agencies**:
  - Simplifies candidate evaluation processes by automating personality analysis.
- **HR Departments**:
  - Efficiently screens job applicants based on personality traits aligned with specific job roles.
- **Employers/Managers**:
  - Facilitates informed decisions in selecting candidates who fit company culture and job requirements.

## Conclusion

The Personality Prediction System is a sophisticated tool that amalgamates machine learning, NLP, and web technologies to streamline the hiring process. By automating personality assessment and leveraging AI for trait description, this system empowers recruiters and employers to make better-informed hiring decisions.
