from flask import request, jsonify
from utils.ota_think import OTA_Think
from constants.llm_constants import SYS_PROMPT1
from constants.sys_prompt_constants import *

def completions():
    if request.is_json:
        content = request.get_json()
        print("Received JSON:", content)
        messages = content.get('messages')
        if messages and isinstance(messages, list) and len(messages) > 0:
            user_message = messages[0].get('content')
            if user_message:
                print("User message:", user_message) 
                global SYS_PROMPT1
                with open(SYS_PROMPT_PATH, 'r') as file:
                    SYS_PROMPT1 = file.read()                
                response_message = OTA_Think(SYS_PROMPT1, user_message)
                response = response_message
                return response
            else:
                return jsonify({'error': 'No content in message'}), 400
        else:
            return jsonify({'error': 'No messages provided'}), 400
    else:
        return jsonify({'error': 'Invalid Content-Type, please send JSON'}), 400
