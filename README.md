# Gemini Predict Serve
This is a prediction module for detecting web application vulnerabilities used for gemini-self-protector

## Gemini System Architecture

![image](https://github.com/noobpk/gemini-predict-serve/assets/31820707/a27b066c-b1b5-435d-9bc8-1f773b6d45a0)

## Web Application Vulnerabilities Detection 

This is a detection method that using combine Convolutional Neural Network (CNN) and a family of Recurrent Neural Network (RNN) to analyze features and relationships in requests from users and predict whether they are vulnerability or not.

## Vulnerabilities Detection

-  Cross-Site Scripting
- SQL Injection
- Path Traversal (LFI)
- Command Injection
- Remote File Inclusion (RFI)
- Json & XML Injection
- HTML5 Injection
- Server Side Includes (SSI) Injection

## Get this image
Obtain the latest Gemini Predict Serve image by executing the following command:

```
docker pull noobpk/gemini-predict-serve:latest
```

## Launching through the Command Line:
Initiate the Predict Serve with the command line using Docker. Choose the appropriate configuration based on your needs:

For basic usage without Kafka streaming:

```
docker run --name gemini-predict-serve -p 5000:443 --rm -e AUTH_KEY=your-authen-key gemini-predict-serve
```

If you have an Apache Kafka server and want to enable streaming:

```
docker run --name gemini-predict-serve -p 5000:443 --rm  \
    -e AUTH_KEY=your-authen-key \
    -e ENABLE_KAFKA_STREAMING=True \
    -e KAFKA_BOOTSTRAP_SERVER=your-kafka-server \
    -e KAFKA_TOPIC=gemini-data-streaming \
    -e KAFKA_USERNAME= \
    -e KAFKA_PASSWORD= \
    -e KAFKA_SECURITY_PROTOCOL=PLAINTEXT \
    gemini-predict-serve
```

## Simplified Deployment with Docker Compose

For an even more streamlined deployment process, Docker Compose provides a user-friendly alternative:

### 1. Download the Docker Compose File:

Acquire the `docker-compose.yml` file from the repository onto your local machine or any system with Docker installed:

```
wget -O docker-compose.yml https://raw.githubusercontent.com/noobpk/gemini-predict-serve/main/docker-compose.yml
```

### 2. Run the Containers:

Navigate to the directory containing the docker-compose.yml file using your terminal and execute the following command:

```
docker-compose up
```

## Configuration

Setup with the Gemini Predict Serve Docker image using the following environment variables:

- `AUTH_KEY` : Authentication key for predict API
- `ENABLE_KAFKA_STREAMING` : Enable send message to kafka. Defaults: False
- `KAFKA_BOOTSTRAP_SERVER` : Kafka server. Example : localhost:9092
- `KAFKA_TOPIC` : Kafka topic. Defaults: gemini-data-streaming
- `KAFKA_USERNAME` : Kafka username
- `KAFKA_PASSWORD` : Kafka password
- `KAFKA_SECURITY_PROTOCOL` : Kafka security protocol. Required

## Ping Pong
```
curl --location 'https://127.0.0.1:5000/ping' --insecure \
--header 'Authorization: your-authen-key'
```

## Predict 

```
$ curl --location 'https://127.0.0.1:5000/predict' --insecure \
--header 'Authorization: your-authen-key' \
--header 'Content-Type: application/json' \
--data '{"data":"../../../../etc/passwd"}'
```

## Kafka Extensions

### Real time Predict Plot

![realtime_plot](https://github.com/noobpk/gemini-predict-serve/assets/31820707/f8f4830b-4a8b-4cea-b986-ea843da3782b)

## More About Repository
Github: [gemini-predict-serve](https://github.com/noobpk/gemini-predict-serve)

Image Issues: [Find or create an issues](https://github.com/noobpk/gemini-predict-serve/issues)
