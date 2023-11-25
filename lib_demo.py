from flask import Flask
from flask_cors import CORS
from utils.csv_utils import *
import routes.local_faq_handler as FAQ_handler
import routes.ota_request_handler as OTA_handler

# Flask app initialization
app = Flask(__name__)
CORS(app)
app.add_url_rule('/v1/chat/completions', 'completions', OTA_handler.completions, methods=['POST'])
app.add_url_rule('/api/libfaq', 'get_csv', FAQ_handler.get_csv, methods=['GET'])
app.add_url_rule('/api/libfaq/submit', 'set_csv', FAQ_handler.set_csv, methods=['POST'])
app.add_url_rule('/api/libfaq/edit', 'edit_csv_row', FAQ_handler.edit_csv_row, methods=['POST'])
app.add_url_rule('/api/libfaq/delete', 'delete_csv_row', FAQ_handler.delete_csv_row, methods=['POST'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
