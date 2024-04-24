import os
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


def analyze_content(content):

    # Create an output parser
    output_parser = StrOutputParser()

    # Analyze content based on multiple prompts
    analysis_results = []
    # Process and print results for each prompt
    for prompt_text in prompts:
        # Create a prompt template
        prompt = ChatPromptTemplate.from_template(
            f"Q: {prompt_text}\nCode: \n{{code_snippet}}"
        )
        # Combine prompt with the language model and output parser
        chain = prompt | google_llm | output_parser
        # Invoke the language model chain with the code snippet
        result = chain.invoke({"code_snippet": content})
        # Print the result
        analysis_results.append(f"Result for '{prompt_text}':\n{result}\n")

    return "\n".join(analysis_results)


def process_files():
    base_dir = "SANSTOP25"
    results_dir = "results"

    # Ensure the results directory exists
    os.makedirs(results_dir, exist_ok=True)
    print(f"Results directory '{results_dir}' is ready.")

    # Iterate over each subdirectory in the base directory
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)

        # Check if it's a directory
        if os.path.isdir(subdir_path):
            # Prepare a results subfolder path
            result_subdir = os.path.join(results_dir, subdir)
            os.makedirs(result_subdir, exist_ok=True)
            print(f"Processing directory '{subdir}'...")

            # Process each file in the subdirectory
            for file in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file)
                print(f"Analyzing file '{file}'...")

                # Open and read the file content
                with open(file_path, "r") as f:
                    content = f.read()

                # Perform analysis
                result = analyze_content(content)
                print(f"Analysis complete for '{file}'. Writing results...")

                # Write the analysis results to a new file in the results subdirectory
                result_file_path = os.path.join(result_subdir, file + ".analysis.md")
                with open(result_file_path, "w") as result_file:
                    result_file.write(result)
                print(f"Results written for '{file}' in '{result_file_path}'.")

    print("All files processed successfully.")


if __name__ == "__main__":
    process_files()
