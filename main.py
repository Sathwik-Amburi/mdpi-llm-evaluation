import os
import logging
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# from langchain_google_vertexai import ChatVertexAI
from langchain_openai import AzureChatOpenAI

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
load_dotenv()

# Define multiple prompts to analyze the code
prompts = [
    "Please explain what this code does.",
    "Is there a vulnerability in this code? Yes or No?",
    "What is the vulnerability in this code? Please provide the CWE number if possible.",
    "Please suggest a fix for this code.",
    "Are there any other vulnerabilities in the code? If yes, please explain and suggest fixes.",
]


def analyze_content(content):
    try:
        # Initialize the Google Vertex AI language model
        # google_llm = ChatVertexAI(model_name="gemini-1.0-pro", cache=False)
        llm = AzureChatOpenAI(deployment_name="codesageai")

        # Create an output parser
        output_parser = StrOutputParser()

        # Analyze content based on multiple prompts
        analysis_results = []
        for prompt_text in prompts:
            prompt = ChatPromptTemplate.from_template(
                f"Q: {prompt_text}\nCode: \n{{code_snippet}}"
            )
            chain = prompt | llm | output_parser
            result = chain.invoke({"code_snippet": content})
            analysis_results.append(f"\n # Result for '{prompt_text}':\n{result}\n")
        return "\n".join(analysis_results)
    except Exception as e:
        logging.error(f"Error processing content: {str(e)}")
        return "Analysis failed"


def process_files():
    base_dir = "SANSTOP25"
    results_dir = "results"

    if not os.path.exists(base_dir):
        logging.error(f"The directory {base_dir} does not exist.")
        return

    os.makedirs(results_dir, exist_ok=True)
    logging.info(f"Results directory '{results_dir}' is ready.")

    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.isdir(subdir_path):
            result_subdir = os.path.join(results_dir, subdir)
            os.makedirs(result_subdir, exist_ok=True)
            logging.info(f"Processing directory '{subdir}'...")

            for file in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file)
                logging.info(f"Analyzing file '{file}'...")
                with open(file_path, "r") as f:
                    content = f.read()

                result = analyze_content(content)
                result_file_path = os.path.join(result_subdir, file + ".analysis.md")
                with open(result_file_path, "w") as result_file:
                    result_file.write(result)
                logging.info(f"Results written for '{file}' in '{result_file_path}'.")

    logging.info("All files processed successfully.")


if __name__ == "__main__":
    process_files()
