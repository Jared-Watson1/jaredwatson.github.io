from embedding import pineconeFilter
from metapub import PubMedFetcher
import pandas as pd
import openai
import json
import os
from dotenv import load_dotenv
load_dotenv()
NCBI_API_KEY = os.getenv("NCBI_API_KEY")


openai.api_key = os.getenv("OPENAI_API_KEY")
fineTunedModel = "davinci:ft-personal-2022-12-30-20-49-43"

fetch = PubMedFetcher()
gpt4 = "gpt-4-0314"
gptTurbo = "gpt-3.5-turbo"


def addToFineTune(prompt, completion, file="data/questionsCreator.jsonl"):
    with open(file, "a") as f:
        data = {"prompt": prompt, "completion": completion}
        f.write(json.dumps(data) + "\n")


def jared_bot(prompt):
    filter = pineconeFilter(prompt, topK=3)
    context = filter[0]
    p = f"""
    Context: {context}

    Question: ### {prompt} ###
    """

    response = openai.ChatCompletion.create(
        model=gptTurbo,
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant chatGPT AI trained on a large amount of medical literature who will assist individuals with their medical questions.  You will use the medical context provided to help form your answers.  Answer the question with the necessary information but be concise."},
            {"role": "user", "content": p},
        ]
    )
    answer = response['choices'][0]['message']['content'] + f"\nPM IDs: {str(filter[1])}"
    
    return answer, filter[1]
