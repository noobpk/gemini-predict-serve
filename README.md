# Gemini-Web Vulnerability Detection (G-WVD)
This is a Gemini-Web Vulnerability Detection (G-WVD) for detecting web application vulnerabilities used for gemini-self-protector

## Gemini Components

![image](https://github.com/noobpk/gemini-web-vulnerability-detection/assets/31820707/4f38e403-b5f4-40a8-8823-def4353a813f)

👉 G-SP : [gemini-self-protector](https://github.com/noobpk/gemini-self-protector)

👉 G-WVD : [gemini-web-vulnerability-detection](https://github.com/noobpk/gemini-web-vulnerability-detection)

👉 G-BD : [gemini-bigdata](https://github.com/noobpk/gemini-bigdata)

## Web Application Vulnerabilities Detection

This is a detection method that using combine Convolutional Neural Network (CNN) and a family of Recurrent Neural Network (RNN) to analyze features and relationships in requests from users and predict whether they are vulnerability or not.

## Vulnerabilities Detection

- Cross-Site Scripting
- SQL Injection
- Path Traversal (LFI)
- Command Injection
- Remote File Inclusion (RFI)
- Json & XML Injection
- HTML5 Injection
- Server Side Includes (SSI) Injection

## Get this image

Docker image : [gemini-web-vulnerability-detection](https://hub.docker.com/r/noobpk/gemini-web-vulnerability-detection)

Obtain the latest G-WVD image by executing the following command:

```
docker pull noobpk/gemini-web-vulnerability-detection:latest
```

## Launching through the Command Line:
Initiate the G-WVD with the command line using Docker. Choose the appropriate configuration based on your needs:

For basic usage without Kafka streaming:

```
docker run --name g-wvd-serve -p 5000:443 --rm -e AUTH_KEY=your-authen-key gemini-web-vulnerability-detection
```

If you have an Apache Kafka server and want to enable streaming:

```
docker run --name g-wvd-serve -p 5000:443 --rm  \
    -e AUTH_KEY=your-authen-key \
    -e ENABLE_KAFKA_STREAMING=True \
    -e KAFKA_BOOTSTRAP_SERVER=your-kafka-server \
    -e KAFKA_TOPIC=gemini-data-streaming \
    -e KAFKA_USERNAME= \
    -e KAFKA_PASSWORD= \
    -e KAFKA_SECURITY_PROTOCOL=PLAINTEXT \
    gemini-web-vulnerability-detection
```

## Simplified Deployment with Docker Compose

For an even more streamlined deployment process, Docker Compose provides a user-friendly alternative:

### 1. Download the Docker Compose File:

Acquire the `docker-compose.yml` file from the repository onto your local machine or any system with Docker installed:

```
wget -O docker-compose.yml https://raw.githubusercontent.com/noobpk/gemini-web-vulnerability-detection/main/docker-compose.yml
```

### 2. Run the Containers:

Navigate to the directory containing the docker-compose.yml file using your terminal and execute the following command:

```
docker-compose up
```

## Configuration

Setup with the G-WVD Docker image using the following environment variables:

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

## More About Repository
Github: [gemini-web-vulnerability-detection](https://github.com/noobpk/gemini-web-vulnerability-detection)

Image Issues: [Find or create an issues](https://github.com/noobpk/gemini-web-vulnerability-detection/issues)
