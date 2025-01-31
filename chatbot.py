import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI  # Corrected import
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# Set up Gemini API Key
genai.configure(api_key="AIzaSyAiAAE5rJOS3petrAK9dqqBk10KvPkyKJE")

# Initialize Gemini model using LangChain
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyAiAAE5rJOS3petrAK9dqqBk10KvPkyKJE")

# Create a prompt template
prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful chatbot. Answer the question: {question}"
)

# Create a chain
chain = LLMChain(llm=llm, prompt=prompt)

# Chatbot loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = chain.run(user_input)
    print("Bot:", response)
