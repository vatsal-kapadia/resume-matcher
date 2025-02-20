from flask import Flask, request, jsonify
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
from dotenv import load_dotenv
import json
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client

def process_large_text(text):
    # Remove any extra whitespace and normalize line endings
    return ' '.join(text.strip().split())   

# Define the route for the API
@app.route('/generate', methods=['POST'])
def generate():
    # Get the resume and job description from the request
    data = request.get_json()

    # Extract and process resume and job description as large strings
    resume = process_large_text(data.get('resume', ''))
    job_description = process_large_text(data.get('job_description', ''))

    # Validate that both fields are provided and not empty
    if not resume or not job_description:
        return jsonify({
            'error': 'Both resume and job description are required'
        }), 400
    # # Get the resume and job description from the request
    # data = request.json
    # resume = data.get('resume') 
    # job_description = data.get('job_description')


    # Generate the customized resume and cover letter
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
    messages=[
        {"role": "system", "content": "You are a resume and cover letter generator. You will be given a resume and a job description. You will need to generate a customized resume and cover letter based on the job description in a JSON format. You also have to calculate the job alignment scrore in percentage between 0 and 100 between the resume and the job description in JSON format."},
        {"role": "user", "content": f"Resume: {resume}\nJob Description: {job_description}"}
    ],
    response_format={"type": "json_object"})     

    # Parse the response
    print(response.choices[0].message.content)
    response_json = json.loads(response.choices[0].message.content)

    # Extract the resume and cover letter from the response 
    resume = response_json.get('resume')
    cover_letter = response_json.get('cover_letter')    
    alignment_score = response_json.get('alignment_score')
    # Return the response
    return jsonify({
        'resume': resume,
        'cover_letter': cover_letter,
        'alignment_score': alignment_score
    })      

if __name__ == '__main__':
    app.run(debug=True)





