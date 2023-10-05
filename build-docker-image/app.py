
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import json
from datetime import datetime
from waitress import serve
from dotenv import load_dotenv
from kafka import KafkaProducer
import ipaddress
from hashlib import sha256

load_dotenv()

AUTH_KEY = os.getenv("AUTH_KEY")
ENABLE_KAFKA_STREAMING = os.getenv("ENABLE_KAFKA_STREAMING")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
KAFKA_SECURITY_PROTOCOL = os.getenv("KAFKA_SECURITY_PROTOCOL")

# Init Flask app
app = Flask(__name__)

CORS(app)

gemini_model = load_model('gemini.keras')

def validate_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return str(ip_obj)  # Return the validated IP address
    except ValueError:
        return "UNKNOWN"  # Return "UNKNOWN" for invalid addresses

def kafka_send_message(key, payload):
    try:
        producer.send(KAFKA_TOPIC, key=key, value=payload)
        producer.flush()
    except Exception as e:
        return jsonify({
            "status": "Exception",
            "message": "{}".format(e)
        }), 500

@app.route('/ping', methods=['GET'])
def server_info():
    authorization_header = request.headers.get('Authorization')
    if str(authorization_header) == str(AUTH_KEY):
        return jsonify({
            "model": "Gemini-Web-Vulnerability-Detection",
            "max_input_length": "unlimit",
            "vector_size": "384",
            "model_build_at": "2023-08-01",
            "encoder": "sentence-transformers/all-MiniLM-L6-v2",
            "docker_image_version": "1.5",
            "extension": "kafka",
            "author": "noobpk - lethanhphuc"
        }), 200
    else:
        return jsonify({
            "message": "UnAuthenticated"
        }), 401

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
                hash_encode_input = sha256(encode_input).hexdigest()
                if str(ENABLE_KAFKA_STREAMING) == 'True':
                    input_ip = request.json['ip']
                    validated_ip = validate_ip(input_ip)
                    now = datetime.now()
                    key_prediction_data = b'prediction_data'
                    payload_prediction_data = {
                        'time': now.strftime('%Y-%m-%d %H:%M:%S'),
                        'ipaddress': validated_ip,
                        'payload': input_string,
                        'score': accuracy_value,
                        'hash': hash_encode_input
                        }
                    kafka_send_message(key_prediction_data, payload_prediction_data)
                return jsonify({
                        "status": "Success",
                        "prediction": input_string,
                        "accuracy": accuracy_value,
                        "hash": hash_encode_input
                    }), 200
            else:
                return jsonify({
                    "status": "Fail",
                    "message": "Unknown request type."
                }), 400
        else:
            return jsonify({
                "message": "UnAuthenticated"
            }), 401
    except Exception as e:
        return jsonify({
            "status": "Exception",
            "message": "{}".format(e)
        }), 500

if __name__ == '__main__':
    for i in tqdm(range(1000), colour="green", desc='Encoder Loading'):
        model_name_or_path = os.environ.get(
        'model_name_or_path', "sentence-transformers/all-MiniLM-L6-v2")
    encoder = SentenceTransformer(model_name_or_path=model_name_or_path)
    if str(ENABLE_KAFKA_STREAMING) == 'True':
        for i in tqdm(range(100), colour="green", desc='Kafka Loading'):
            producer = KafkaProducer(
                bootstrap_servers = [KAFKA_BOOTSTRAP_SERVER],
                sasl_plain_username = KAFKA_USERNAME,
                sasl_plain_password = KAFKA_PASSWORD,
                security_protocol = KAFKA_SECURITY_PROTOCOL,
                value_serializer = lambda v: json.dumps(v).encode('utf-8')
                )
    print("[+] Serve Started Successfull")
    serve(app, host='0.0.0.0', port=5000)
