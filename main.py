from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI

# Load environment variables
load_dotenv()

# Initialize the Google Vertex AI language model
google_llm = ChatVertexAI(model_name="gemini-1.5-pro-preview-0409")

# Define multiple prompts to analyze the code
prompts = [
    "Please explain what this code does.",
    "Is there a vulnerability in this code? Yes or No?",
    "What is the vulnerability in this code? Please provide the CWE number if possible.",
    "Please suggest a fix for this code.",
    "Are there any other vulnerabilities in the code? If yes, please explain and suggest fixes.",
]

# Setup for reading code from a file
with open("sample_example.c", "r") as f:
    code_snippet = f.read()

# Create an output parser
output_parser = StrOutputParser()

# Process and print results for each prompt
for prompt_text in prompts:
    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(
        f"Q: {prompt_text}\nCode: \n{{code_snippet}}"
    )
    # Combine prompt with the language model and output parser
    chain = prompt | google_llm | output_parser
    # Invoke the language model chain with the code snippet
    result = chain.invoke({"code_snippet": code_snippet})
    # Print the result
    print(f"Result for '{prompt_text}': {result}\n")
