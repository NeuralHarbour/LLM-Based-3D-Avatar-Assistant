from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
import google.generativeai
import os

async def generate_palm_embedding(prompt):
    API_KEY = open('PALM_api.txt', 'r').read()
    
    llm = GooglePalm(google_api_key=API_KEY)
    llm.temperature = 0.1
    
    prompts = [prompt]
    llm_result = llm._generate(prompts)
    
    return llm_result.generations[0][0].text

# Example usage
prompt = 'Explain the difference between effective and affective with examples'
result = generate_palm_embedding(prompt)
print(result)
