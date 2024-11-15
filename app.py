from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_test_case_with_steps(story_description):
    prompt = f"Generate test cases with short, realistic steps for the following story:\n\n{story_description}\n\nKeep the steps concise and straightforward."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating test cases with detailed steps."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        test_case_with_steps = response['choices'][0]['message']['content'].strip()
        return test_case_with_steps
    except Exception as e:
        return str(e)

@app.route('/generate-test-case', methods=['POST'])
def generate_test_case():
    data = request.get_json()
    story_description = data.get("story_description", "")
    result = generate_test_case_with_steps(story_description)
    return jsonify({"test_case": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

