from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__, static_folder="static")
CORS(app)  # Enable Cross-Origin Resource Sharing

# Set up Gemini API Key
genai.configure(api_key="AIzaSyAiAAE5rJOS3petrAK9dqqBk10KvPkyKJE")

# Initialize Gemini model using LangChain
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyAiAAE5rJOS3petrAK9dqqBk10KvPkyKJE")

# Create a prompt template
prompt = PromptTemplate(
    input_variables=["question", "user_name", "user_email"],
    template="You are a helpful chatbot. User name is {user_name} and email is {user_email}. Answer the question: {question}"
)

# Create a chain
chain = LLMChain(llm=llm, prompt=prompt)

# Serve the homepage (index.html) from static folder
@app.route('/')
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

# Define an API route for chatting
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    user_details = data.get("userDetails", {})

    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Extract user details
    user_name = user_details.get("name", "User")
    user_email = user_details.get("email", "No email provided")

    # Update the prompt with user details
    response = chain.run(question=user_input, user_name=user_name, user_email=user_email)
    
    return jsonify({"response": response})

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
