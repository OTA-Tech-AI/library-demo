from flask import request, jsonify
from constants.sys_prompt_constants import *
from constants.llm_constants import *
from constants.sys_prompt_constants import *

def edit_sysprompt():
    global SYS_PROMPT1
    try:
        # Read the sys_prompt.txt content
        with open(SYS_PROMPT_PATH, 'r') as file:
            SYS_PROMPT1 = file.read()
        return jsonify({'message': 'System prompt edited successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
def reset_sysprompt():
    global SYS_PROMPT1
    try:
        # Read the default prompt content
        with open(SYS_PROMPT_DEFAULT_PATH, 'r') as file:
            default_content = file.read()
            SYS_PROMPT1 = default_content

        # Overwrite the sys_prompt.txt with default content
        with open(SYS_PROMPT_PATH, 'w') as file:
            file.write(default_content)

        return jsonify({'message': 'System prompt reset successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
