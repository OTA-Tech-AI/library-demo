from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from utils.csv_utils import *

# Constants
INPUTMARKER_END = "-- END --"
ANYSCALE_ENDPOINT_TOKEN = "esecret_hpbtup4hhe4rha63h2ibh2mich"
openai_api_key = "esecret_hpbtup4hhe4rha63h2ibh2mich"
openai_api_base = "https://api.endpoints.anyscale.com/v1"
model_name = "HuggingFaceH4/zephyr-7b-beta"
sys_prompt1 = """
      You are a helpful librarian named OTA. 
      """

# Flask app initialization
app = Flask(__name__)
CORS(app)

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
    "Authorization": f"Bearer {openai_api_key}"
    }
    # input_text = "You should refer to chat history and response my question. " + input_text
    # Set up the data for the API request
    data = {
        "model": model_name,
        "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": input_text}],
        "temperature": 0
    }

    # Make the API request
    print("\n---------------------Prompt is below ---------------------\n")
    print(sys_prompt)
    # Make the HTTP POST request
    response = requests.post(f"{openai_api_base}/chat/completions", headers=headers, data=json.dumps(data))
    response_data = response.json()

    # Extract the response from the API
    prompt_response = response_data["choices"][0]["message"]["content"]
    usage = response_data["usage"]

    # Print the response
    print("\n------------------OTA BRAIN---------------------------\n")
    print(prompt_response)
    print("\n------------------------------------------------------\n")
    return prompt_response

@app.route('/v1/chat/completions', methods=['POST'])
def completions():
    if request.is_json:
        content = request.get_json()
        print("Received JSON:", content)
        messages = content.get('messages')
        if messages and isinstance(messages, list) and len(messages) > 0:
            user_message = messages[0].get('content')
            if user_message:
                print("User message:", user_message)    
                response_message = OTA_Think(sys_prompt1, user_message)
                response = response_message
                return response
            else:
                return jsonify({'error': 'No content in message'}), 400
        else:
            return jsonify({'error': 'No messages provided'}), 400
    else:
        return jsonify({'error': 'Invalid Content-Type, please send JSON'}), 400

@app.route('/api/csv', methods=['GET'])
def get_csv():
    try:
        data = read_csv("data/qa.csv")
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/csv/submit', methods=['POST'])
def set_csv():
    try:
        data = request.json
        if not data.get('question') or not data.get('answer'):
            return jsonify({'error': 'Question and answer fields cannot be empty'}), 400
        data['status'] = 0
        add_row_to_csv('data/qa.csv', data)
        return jsonify({'message': 'Data received successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/csv/edit', methods=['POST'])
def edit_csv_row():
    try:
        data = request.json
        old_data = data.get('old_data')
        new_data = data.get('new_data')
        index = old_data.get('index')
        question = old_data.get('question')
        answer = old_data.get('answer')

        if index is None:
            return jsonify({'error': 'Index is required'}), 400

        # Convert index to integer if it's passed as a string
        index = int(index)
        if modify_row_in_csv_by_index('data/qa.csv', index, question, answer, new_data):
            return jsonify({'message': 'Row deleted successfully'}), 200
        else:
            return jsonify({'error': 'Row not found or could not be deleted'}), 404
    except ValueError:
        return jsonify({'error': 'Invalid index format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/csv/delete', methods=['POST'])
def delete_csv_row():
    try:
        data = request.json
        index = data.get('index')
        question = data.get('question')
        answer = data.get('answer')
        if index is None:
            return jsonify({'error': 'Index is required'}), 400

        # Convert index to integer if it's passed as a string
        index = int(index)
        if delete_row_from_csv_by_index('data/qa.csv', index, question, answer):
            return jsonify({'message': 'Row deleted successfully'}), 200
        else:
            return jsonify({'error': 'Row not found or could not be deleted'}), 404
    except ValueError:
        return jsonify({'error': 'Invalid index format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
