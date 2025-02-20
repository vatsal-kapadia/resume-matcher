from flask import Flask, request, jsonify, Response
import openai
import os
from dotenv import load_dotenv
import json
from flask_cors import CORS  # Import CORS

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)

# Function to process large text input
def process_large_text(text):
    return ' '.join(text.strip().split())

@app.route('/generate', methods=['POST'])
def generate():
    # Get the resume and job description from the request
    data = request.get_json()

    resume = process_large_text(data.get('resume', ''))
    job_description = process_large_text(data.get('job_description', ''))

    if not resume or not job_description:
        return jsonify({
            'error': 'Both resume and job description are required'
        }), 400

    # Generate the customized resume and cover letter
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a resume and cover letter generator. You will be given a resume and a job description. You will need to generate and suggest some changes to the resume and generate a new cover letter based on the job description in a JSON format. You also have to calculate the job alignment score in percentage between 0 and 100 between the resume and the job description in JSON format."},
            {"role": "user", "content": f"Resume: {resume}\nJob Description: {job_description}"}
        ],
        response_format={"type": "json_object"}
    )     

    print("Raw OpenAI API response:", response)


    # Parse the response
    response_json = json.loads(response.choices[0].message.content) 
    print("Parsed response:", response_json)


    # Extract the resume, cover letter, and alignment score from the response
    resume = response_json.get('resume') 
    cover_letter = response_json.get('cover_letter')    
    alignment_score = response_json.get('alignment_score')

    output_text = f"Resume:\n{resume}\n\nCover Letter:\n{cover_letter}\n\nAlignment Score: {alignment_score}%" 
    print("Output text:", output_text)


    # Return the plain text response
    return Response(output_text, mimetype='text/plain') 


    return jsonify({
        'resume': resume,
        'cover_letter': cover_letter,
        'alignment_score': 'placeholder' 
    })

if __name__ == '__main__':
    app.run(debug=True)
