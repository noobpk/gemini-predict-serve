
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from sentence_transformers import SentenceTransformer
import numpy as np
from waitress import serve
from dotenv import load_dotenv

load_dotenv()

AUTH_KEY = os.getenv("AUTH_KEY")

# Init Flask app
app = Flask(__name__)

CORS(app)

gemini_model = load_model('gemini.keras')

@app.route('/ping', methods=['GET'])
def server_info():
    authorization_header = request.headers.get('Authorization')
    if str(authorization_header) == str(AUTH_KEY):
        return jsonify({
            "model": "Gemini-Web-Vuln-Detect",
            "max_input_length": "unlimit",
            "vector_size": "384",
            "model_build_at": "2023-08-01",
            "encoder": "sentence-transformers/all-MiniLM-L6-v2",
            "docker_image_version": "1.3",
            "author": "noobpk - lethanhphuc"
        })
    else:
        return jsonify({
            "message": "UnAuthenticated"
        })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        authorization_header = request.headers.get('Authorization')

        if str(authorization_header) == str(AUTH_KEY):
            if request.is_json:
                # get input from json
                input_string = request.json['data']
                # Encode the input string and reshape
                encode_input = encoder.encode(input_string).reshape((1,384))
                prediction = gemini_model.predict(encode_input)
                accuracy = prediction * 100
                accuracy_value = float(accuracy[0][0])
                return jsonify({
                        "status": "Success",
                        "prediction": input_string,
                        "accuracy": accuracy_value
                    })
            else:
                return jsonify({
                    "status": "Fail",
                    "message": "Unknown request type."
                })
        else:
            return jsonify({
                "message": "UnAuthenticated"
            })
    except Exception as e:
        return jsonify({
            "status": "Exception",
            "message": "{}".format(e)
        })

if __name__ == '__main__':
    print("[+] Service Started")
    model_name_or_path = os.environ.get(
        'model_name_or_path', "sentence-transformers/all-MiniLM-L6-v2")
    encoder = SentenceTransformer(model_name_or_path=model_name_or_path)
    serve(app, host='0.0.0.0', port=5000)
