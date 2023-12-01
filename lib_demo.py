from flask import Flask
from flask_cors import CORS
from utils.csv_utils import *
from constants.sys_prompt_constants import *
import routes.local_faq_handler as FAQ_handler
import routes.local_knowledge_handler as Knowledge_handler
import routes.ota_request_handler as OTA_handler
import routes.ota_sys_prompt_handler as Sys_Prompt_handler

# Flask app initialization
app = Flask(__name__)
CORS(app)

# OTA Action Handler
app.add_url_rule('/v1/chat/completions', 'completions', OTA_handler.completions, methods=['POST'])

# library FAQ page
app.add_url_rule('/api/libfaq', 'faq_get_csv', FAQ_handler.get_csv, methods=['GET'])
app.add_url_rule('/api/libfaq/submit', 'faq_set_csv', FAQ_handler.set_csv, methods=['POST'])
app.add_url_rule('/api/libfaq/edit', 'faq_edit_csv_row', FAQ_handler.edit_csv_row, methods=['POST'])
app.add_url_rule('/api/libfaq/delete', 'faq_delete_csv_row', FAQ_handler.delete_csv_row, methods=['POST'])

# library general knowledge base
app.add_url_rule('/api/libknowledge', 'knowledge_get_csv', Knowledge_handler.get_csv, methods=['GET'])
app.add_url_rule('/api/libknowledge/submit', 'knowledge_set_csv', Knowledge_handler.set_csv, methods=['POST'])
app.add_url_rule('/api/libknowledge/edit', 'knowledge_edit_csv_row', Knowledge_handler.edit_csv_row, methods=['POST'])
app.add_url_rule('/api/libknowledge/delete', 'knowledge_delete_csv_row', Knowledge_handler.delete_csv_row, methods=['POST'])

# update and reset system prompt
app.add_url_rule('/api/sysprompt', 'sys_prompt_get', Sys_Prompt_handler.get_sysprompt, methods=['GET'])
app.add_url_rule('/api/sysprompt/edit', 'sys_prompt_edit', Sys_Prompt_handler.edit_sysprompt, methods=['POST'])
app.add_url_rule('/api/sysprompt/reset', 'sys_prompt_reset', Sys_Prompt_handler.reset_sysprompt, methods=['POST'])

if __name__ == '__main__':
    app.run(port=5000, debug=False)
