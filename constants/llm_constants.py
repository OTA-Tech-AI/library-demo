from constants.sys_prompt_constants import *

### LLM Server ###
ANYSCALE_ENDPOINT_TOKEN = "esecret_hpbtup4hhe4rha63h2ibh2mich"
OPENAI_API_KEY = "esecret_hpbtup4hhe4rha63h2ibh2mich"
OPENAI_API_BASE = "https://api.endpoints.anyscale.com/v1"
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

### Prompt ###
INPUTMARKER_END = "-- END --"
global SYS_PROMPT1
with open(SYS_PROMPT_PATH, 'r') as file:
    SYS_PROMPT1 = file.read()