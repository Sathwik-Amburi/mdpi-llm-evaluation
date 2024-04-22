from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

llm = AzureChatOpenAI(deployment_name="codesageai")

#prompt
prompt = ChatPromptTemplate.from_template("Q: What does this code do: \n {code_snippet}")
output_parser = StrOutputParser()


chain = prompt | llm | output_parser

f = open("sample_example.c","r")
code_snippet = f.read()

input = {"code_snippet": code_snippet}

print(prompt.invoke(input))

# # # Run the LLM
print(chain.invoke(input))
