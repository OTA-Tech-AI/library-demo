from flask import request, jsonify
from utils.csv_utils import *
from constants.learningdb_constants import LIB_FAQ_CSV_PATH

def get_csv():
    try:
        data = read_csv(LIB_FAQ_CSV_PATH)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def set_csv():
    try:
        data = request.json
        if not data.get('question') or not data.get('answer'):
            return jsonify({'error': 'Question and answer fields cannot be empty'}), 400
        data['status'] = 0
        add_row_to_csv(LIB_FAQ_CSV_PATH, data)
        return jsonify({'message': 'Data received successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        if modify_row_in_csv_by_index(LIB_FAQ_CSV_PATH, index,
                                      ["question", "answer"],
                                      [question, answer],
                                      new_data):
            return jsonify({'message': 'Row deleted successfully'}), 200
        else:
            return jsonify({'error': 'Row not found or could not be deleted'}), 404
    except ValueError:
        return jsonify({'error': 'Invalid index format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        if delete_row_from_csv_by_index(LIB_FAQ_CSV_PATH, index,
                                        ["question", "answer"],
                                        [question, answer]):
            return jsonify({'message': 'Row deleted successfully'}), 200
        else:
            return jsonify({'error': 'Row not found or could not be deleted'}), 404
    except ValueError:
        return jsonify({'error': 'Invalid index format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500