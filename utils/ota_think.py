from flask_cors import CORS
import requests
import json
import pandas as pd
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from utils.csv_utils import *
from constants.llm_constants import *
from constants.learningdb_constants import *

embeddings = HuggingFaceEmbeddings()
db = FAISS.load_local("faiss_index", embeddings)

def retrieve_info(query):
    similar_response = db.similarity_search(query, k=2)
    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array

def OTA_Think(sys_prompt,input_text):
    df_qa = pd.read_csv(LIB_FAQ_CSV_PATH, index_col=0, encoding='ISO-8859-1')
    df_knowledge = pd.read_csv(LIB_KNOWLEDGE_CSV_PATH, index_col=0, encoding='ISO-8859-1')
    filtered_df_qa = df_qa[df_qa['status'] == 0]
    filtered_df_knowledge = df_knowledge[df_knowledge['status'] == 0]

    # Ensure all data is in string format
    filtered_df_qa = filtered_df_qa.astype(str)
    filtered_df_knowledge = filtered_df_knowledge.astype(str)

    # Format the strings with labels and new lines
    combined_qa = filtered_df_qa.apply(lambda x: f"Question: {x['question']}\nAnswer: {x['answer']}\n", axis=1)
    combined_knowledge = filtered_df_knowledge.apply(lambda x: f"Title: {x['title']}\nKnowledge: {x['knowledge']}\n", axis=1)

    # Convert to string
    combined_qa_str = '\n'.join(combined_qa)
    combined_knowledge_str = '\n'.join(combined_knowledge)

    # Concatenate the two strings with a newline in between
    final_combined_string = combined_qa_str + '\n' + combined_knowledge_str

    sys_prompt = sys_prompt + "\nPlease refer to the information below to chat with the user. PLease ignore irrelevant information. \n" \
        + final_combined_string + "".join([item + "\n" for item in retrieve_info(input_text)]) 
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
