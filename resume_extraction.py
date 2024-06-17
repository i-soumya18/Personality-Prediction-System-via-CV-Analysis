import os
import PyPDF2
import textract
import spacy
import re
from docx import Document
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk



nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text


def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            text = ''
            for page in range(num_pages):
                text += pdf_reader.pages[page].extract_text()
        return text
    except PyPDF2.utils.PdfReadError:
        text = textract.process(file_path).decode('utf-8')
        return text


def preprocess_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenization
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # Join tokens back into text
    preprocessed_text = ' '.join(lemmatized_tokens)
    return preprocessed_text


def extract_text_based_on_file(file_path):
    if file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        text = "Unsupported file format for file: {}".format(file_path)

    # Perform text preprocessing
    preprocessed_text = preprocess_text(text)
    return preprocessed_text


def extract_features_from_resumes(folder_path):
    extracted_texts = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            text = extract_text_based_on_file(file_path)
            extracted_texts.append(text)
    return extracted_texts


def extract_tfidf_features(texts):
    # Initialize the TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # Adjust max_features as needed

    # Fit and transform the text
    tfidf_features = tfidf_vectorizer.fit_transform(texts)
    return tfidf_features, tfidf_vectorizer




def extract_name(filename, row_number):
    # Extract name from the PDF filename
    name_pattern = r'(.+?)\.pdf'  # Pattern to match the name before '.pdf'

    # Search for the name pattern in the filename
    match = re.search(name_pattern, filename)

    if match:
        extracted_name = match.group(1)  # Extract the name without the '.pdf'
    else:
        extracted_name = f"resume_{row_number}"  # Return row_number if name not found

    return extracted_name






import re

def extract_contact_info(text):
    # Email extraction pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # Phone number extraction pattern (supports various formats)
    phone_pattern = r'\b(?:\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}\b|\d{4}[-.\s]??\d{3}[-.\s]??\d{4}\b)'

    # Find email addresses in the text
    emails = re.findall(email_pattern, text)
    # Find phone numbers in the text
    phones = re.findall(phone_pattern, text)

    # Combine email addresses and phone numbers as contact information
    contact_info = ', '.join(emails + phones)

    return contact_info



def extract_education(text):
    # Read education keywords from a file
    with open('education.txt', 'r', encoding='utf-8') as file:
        education_keywords = file.read().splitlines()

    # Convert text to lowercase for case-insensitive matching
    lowercase_text = text.lower()

    # Initialize an empty list to store extracted education details
    education_details = []

    # Search for education keywords in the text
    for keyword in education_keywords:
        if keyword.lower() in lowercase_text:
            education_details.append(keyword)

    # Combine the extracted education details into a string
    education_info = ', '.join(education_details)

    return education_info



def extract_work_experience(text, work_exp_file='workExp.txt'):
    # Read work experience keywords from the specified file
    with open(work_exp_file, 'r', encoding='utf-8') as file:
        experience_keywords = file.read().splitlines()

    # Convert text to lowercase for case-insensitive matching
    lowercase_text = text.lower()

    # Initialize an empty list to store extracted work experience details
    experience_details = []

    # Search for work experience keywords in the text
    for keyword in experience_keywords:
        if keyword.lower() in lowercase_text:
            experience_details.append(keyword)

    # Combine the extracted work experience details into a string
    work_experience_info = ', '.join(experience_details)

    return work_experience_info



def extract_skills(text, skills_file='skills.txt'):
    # Read skills from the specified file using UTF-8 encoding
    with open(skills_file, 'r', encoding='utf-8') as file:
        skills_keywords = file.read().splitlines()

    # Convert text to lowercase for case-insensitive matching
    lowercase_text = text.lower()

    # Initialize an empty list to store extracted skills
    skills_list = []

    # Search for skill keywords in the text
    for skill in skills_keywords:
        if skill.lower() in lowercase_text:
            skills_list.append(skill)

    # Combine the extracted skills into a string
    skills_info = ', '.join(skills_list)

    return skills_info






def construct_dataset(folder_path):
    dataset = []
    row_number = 1  # Initialize row number
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            text = extract_text_based_on_file(file_path)
            name = extract_name(filename, row_number)

            # Extract relevant information from the text
            name = extract_name(filename, row_number)
            contact_info = extract_contact_info(text)
            education = extract_education(text)
            work_experience = extract_work_experience(text)
            skills = extract_skills(text)
            row_number += 1

            # Create a dictionary representing a row in the dataset
            resume_data = {
                'Filename': filename,
                'Name': name,
                'Contact Information': contact_info,
                'Education': education,
                'Work Experience': work_experience,
                'Skills': skills,
                # Add other fields accordingly
            }

            dataset.append(resume_data)
    return dataset


def save_dataset_to_csv(dataset, output_file):
    import csv

    # Define the field names (column headers) for the CSV file
    fieldnames = ['Filename', 'Name', 'Contact Information', 'Education', 'Work Experience', 'Skills']
    # Add other field names here if needed

    # Write the dataset to a CSV file
    with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)



if __name__ == "__main__":
    folder_path = (r"C:\Developer\PycharmProjects\personality-Prediction-System-via-CV-Analysis\uploads")
    #folder_path = (r"C:\Developer\PycharmProjects\python-Test-Projects\data\ENGINEERING")


    if not os.path.exists(folder_path):
        print("Folder path doesn't exist.")
    else:
        # Extract preprocessed text from resumes
        extracted_texts = extract_features_from_resumes(folder_path)
        # Extract and structure data from resumes
        dataset = construct_dataset(folder_path)

        # Extract TF-IDF features
        tfidf_features, tfidf_vectorizer = extract_tfidf_features(extracted_texts)

        # Save the structured dataset to a CSV file
        output_file = 'resume_dataset.csv'
        save_dataset_to_csv(dataset, output_file)
        print(f"Dataset saved to {output_file}")

        # Display TF-IDF features
        feature_names = tfidf_vectorizer.get_feature_names_out()
        print("TF-IDF Features:")
        print(feature_names)
        print("\nTF-IDF Matrix:")
        print(tfidf_features.toarray())
