from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import os

import pandas as pd
import csv
from ai_prediction import chat
from resume_extraction import (
    extract_text_based_on_file,
    extract_name,
    extract_contact_info,
    extract_education,
    extract_work_experience,
    extract_skills,
)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

from prediction import assign_personality_traits
@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract text from uploaded resume
            text = extract_text_based_on_file(file_path)

            # Generate a unique row_number using the current timestamp
            row_number = datetime.now().strftime("%Y%m%d%H%M%S")

            # Extract information from the text
            name = extract_name(filename, row_number)
            contact_info = extract_contact_info(text)
            education = extract_education(text)
            work_experience = extract_work_experience(text)
            skills = extract_skills(text)

            # Save the extracted details to a CSV file
            extracted_details = {
                'Filename': filename,
                'Name': name,
                'Contact Information': contact_info,
                'Education': education,
                'Work Experience': work_experience,
                'Skills': skills,
            }
            save_to_csv(extracted_details, 'extracted_details.csv')

            # Get the personality traits
            personality_traits = assign_personality_traits(extracted_details)

            # Add the personality traits to the extracted details
            extracted_details.update(personality_traits)
            # Generate a response from the AI model
            query = "describe a candidate's personality if his traits are: " + ', '.join(
                f"{k}: {v}" for k, v in personality_traits.items())
            response = chat(query)

            # Render the 'result.html' template with extracted details and AI response passed as variables
            return render_template('result.html',
                                   name=name,
                                   contact_info=contact_info,
                                   education=education,
                                   work_experience=work_experience,
                                   skills=skills,
                                   personality_traits=personality_traits,
                                   response=response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    try:
        data = pd.read_csv('extracted_details.csv')
        return data.to_json(orient='records')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        open('extracted_details.csv', 'w').close()  # This will clear the file
        return jsonify({'success': 'History cleared'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_data', methods=['GET'])
def export_data():
    try:
        return send_file('extracted_details.csv', as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def save_to_csv(data, filename):
    try:
        # Check if file exists
        file_exists = os.path.isfile(filename)

        with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header only if file didn't exist
            if not file_exists:
                writer.writerow(data.keys())
            # Write data row
            writer.writerow(data.values())
    except Exception as e:
        print(f"Error occurred while saving to CSV: {e}")

if __name__ == '__main__':
    app.run(debug=True)
