
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
import re
import base64
import html
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

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

gemini_model = load_model('gemini-23-10-23.h5')

def load_encoder():
    for i in tqdm(range(1000), colour="green", desc='Encoder Loading'):
        pass
    model_name_or_path = os.environ.get('model_name_or_path', "sentence-transformers/all-MiniLM-L6-v2")
    encoder = SentenceTransformer(model_name_or_path=model_name_or_path)
    # Perform other encoder-related tasks if needed
    return encoder

def load_kafka_producer():
    if str(ENABLE_KAFKA_STREAMING) == 'True':
        for i in tqdm(range(1000), colour="green", desc='Kafka Loading'):
            pass
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER],
            sasl_plain_username=KAFKA_USERNAME,
            sasl_plain_password=KAFKA_PASSWORD,
            security_protocol=KAFKA_SECURITY_PROTOCOL,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        # Perform other Kafka producer related tasks if needed
        return producer
    else:
        return None

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

def rule_based_detect(_string):
    try:
        rule_based_xss_found = False
        rule_based_sqli_found = False

        """Decode a string using the specified encoding type."""

        # Remove the invalid escape sequences  - # Remove the backslash
        string = _string.replace('\%', '%').replace('\\', '').replace('<br/>', '')

        string = string.encode().decode('unicode_escape')

        string = urllib.parse.unquote(string)

        string = html.unescape(string)

        # Use a regular expression to find all base64-encoded segments in the string
        base64_pattern = r'( |,|;)base64,([A-Za-z0-9+/]*={0,2})'

        # Iterate over the matches and decode the base64-encoded data
        match = re.search(base64_pattern, string)
        if match:
            encoded_string = match.group(2)

            # Try first base64-decode
            try:
                decoded_string = base64.b64decode(encoded_string).decode()
                string = string.replace(encoded_string, decoded_string)
            except:
                pass

            # Try second base64-decode
            try:
                string = string.replace('\%', '%').replace(
                    '\\', '').replace('<br/>', '').replace(' ', '')
                match = re.search(base64_pattern, string)

                if match:
                    encoded_string = match.group(2)
                    try:
                        decoded_string = base64.b64decode(encoded_string).decode()
                        string = string.replace(encoded_string, decoded_string)
                    except:
                        pass
            except:
                pass

        # Use this pattern for detect cross-site scripting
        xss_patterns = [
            r'(?:https?://|//)[^\s/]+\.js'
            r"((\%3C)|<)((\%2F)|\/)*[a-z0-9\%]+((\%3E)|>)",
            r"((\%3C)|<)((\%69)|i|(\%49))((\%6D)|m|(\%4D))((\%67)|g|(\%47))[^\n]+((\%3E)|>)",
            r"((\%3C)|<)[^\n]+((\%3E)|>)"
        ]

        for pattern in xss_patterns:
            matches = re.findall(pattern, string, re.IGNORECASE | re.VERBOSE)
            if matches:
                for match in matches:
                    string = string.replace(match[0], '5dc6f09bb9f90381814ff9fcbfe0a685')
                    rule_based_xss_found = True
                    break

        # Lowercase string
        string = string.lower()

        # Use this pattern for detect sql injection
        sql_patterns = [
            r"(?:select\s+.+\s+from\s+.+)",
            r"(?:insert\s+.+\s+into\s+.+)",
            r"(?:update\s+.+\s+set\s+.+)",
            r"(?:delete\s+.+\s+from\s+.+)",
            r"(?:drop\s+.+)",
            r"(?:truncate\s+.+)",
            r"(?:alter\s+.+)",
            r"(?:exec\s+.+)",
            r"(\s*(all|any|not|and|between|in|like|or|some|contains|containsall|containskey)\s+.+[\=\>\<=\!\~]+.+)",
            r"(?:let\s+.+[\=]\s+.*)",
            r"(?:begin\s*.+\s*end)",
            r"(?:\s*[\/\*]+\s*.+\s*[\*\/]+)",
            r"(?:\s*(\-\-)\s*.+\s+)",
            r"(?:\s*(contains|containsall|containskey)\s+.+)",
            r"\w*((\%27)|('))((\%6F)|o|(\%4F))((\%72)|r|(\%52))",
            r"exec(\s|\+)+(s|x)p\w+"
        ]


        for pattern in sql_patterns:
            matches = re.findall(pattern, string, re.IGNORECASE | re.VERBOSE)
            if matches:
                for match in matches:
                    # select * from noobpk; - 90e87fc8ba835e0d2bfeec5e3799ecfe
                    string = string.replace(
                        match[0], ' 90e87fc8ba835e0d2bfeec5e3799ecfe')
                    rule_based_sqli_found = True
                    break

        return {"xss": rule_based_xss_found, "sqli": rule_based_sqli_found}
    except Exception as e:
        return None

@app.route('/ping', methods=['GET'])
def server_info():
    authorization_header = request.headers.get('Authorization')
    if str(authorization_header) == str(AUTH_KEY):
        return jsonify({
            "model": "Gemini-Web-Vulnerability-Detection",
            "sample": "592479",
            "max_input_length": "unlimit",
            "vector_size": "384",
            "param": "2536417",
            "model_build_at": "2023-10-23",
            "encoder": "sentence-transformers/all-MiniLM-L6-v2",
            "docker_image_version": "1.7",
            "extension": "kafka - rule based detection",
            "author": "noobpk - lethanhphuc"
        }), 200
    else:
        return jsonify({
            "message": "UnAuthenticated"
        }), 401

@app.route('/predict', methods=['POST'])
def process_request():
    try:
        authorization_header = request.headers.get('Authorization')

        if str(authorization_header) == str(AUTH_KEY):
            if request.is_json:
                # get input from json
                input_string = request.json['data']
                # Encode the input string and reshape
                encode_input = encoder.encode(input_string).reshape((1,384))

                def predict():
                    return gemini_model.predict(encode_input)

                def calculate_accuracy(prediction):
                    accuracy = prediction * 100
                    return float(accuracy[0][0])

                def generate_hash():
                    return sha256(encode_input).hexdigest()

                def rule_detection():
                    return rule_based_detect(input_string)

                # Perform prediction, accuracy calculation, hash generation, and rule detection asynchronously using threads
                with ThreadPoolExecutor() as executor:
                    prediction = executor.submit(predict)
                    accuracy = executor.submit(calculate_accuracy, prediction.result())
                    hash_value = executor.submit(generate_hash)
                    rule_detection_result = executor.submit(rule_detection)

                # Get the results
                score_value = accuracy.result()
                hash_encode_input = hash_value.result()
                rule_based_detection = rule_detection_result.result()
                now = datetime.now()

                if str(ENABLE_KAFKA_STREAMING) == 'True':
                    def kafka_task():
                        input_ip = request.json['ip']
                        validated_ip = validate_ip(input_ip)
                        key_prediction_data = b'prediction_data'
                        payload_prediction_data = {
                            'time': now.strftime('%Y-%m-%d %H:%M:%S'),
                            'ipaddress': validated_ip,
                            'payload': input_string,
                            'score': score_value,
                            'hash': hash_encode_input,
                            'rbd_xss': rule_based_detection['xss'],
                            'rbd_sqli': rule_based_detection['sqli'],
                        }
                        kafka_send_message(key_prediction_data, payload_prediction_data)

                    # Perform Kafka message sending in a separate thread
                    with ThreadPoolExecutor() as kafka_executor:
                        kafka_executor.submit(kafka_task)

                return jsonify({
                        "status": "Success",
                        "threat_metrix": {
                            "time": now.strftime('%Y-%m-%d %H:%M:%S'),
                            "prediction": input_string,
                            "score": score_value,
                            "hash": hash_encode_input,
                            "rbd_xss": rule_based_detection['xss'],
                            "rbd_sqli": rule_based_detection['sqli'],
                        }
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
    with ThreadPoolExecutor(max_workers=2) as executor:
        encoder_future = executor.submit(load_encoder)
        kafka_producer_future = executor.submit(load_kafka_producer)

        encoder = encoder_future.result()
        producer = kafka_producer_future.result()

        print("[+] Serve Started Successfully")
        serve(app, host='0.0.0.0', port=5000)
