from flask_cors import CORS
import requests
import json
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from utils.csv_utils import *
from constants.llm_constants import *

embeddings = HuggingFaceEmbeddings()
db = FAISS.load_local("faiss_index", embeddings)

def retrieve_info(query):
    similar_response = db.similarity_search(query, k=2)
    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array

def OTA_Think(sys_prompt,input_text):
    sys_prompt = sys_prompt + "\nPlease look at the chat history as guideline to chat with the user\n" \
        + "".join([item + "\n" for item in retrieve_info(input_text)]) + "\nPLease ignore irrelevant chat history and the student name, you are chatting with a new user. "
    # Set up the API request
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    # input_text = "You should refer to chat history and response my question. " + input_text
    # Set up the data for the API request
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": input_text}],
        "temperature": 0
    }

    # Make the API request
    print("\n---------------------Prompt is below ---------------------\n")
    print(sys_prompt)
    # Make the HTTP POST request
    response = requests.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, data=json.dumps(data))
    response_data = response.json()

    # Extract the response from the API
    prompt_response = response_data["choices"][0]["message"]["content"]
    usage = response_data["usage"]

    # Print the response
    print("\n------------------OTA BRAIN---------------------------\n")
    print(prompt_response)
    print("\n------------------------------------------------------\n")
    return prompt_response
