## Guide Build & Push Docker Image to Docker Hub

### Build Image

`docker build -t gemini-web-vulnerability-detection .`

### Tag and Push Image

`docker tag gemini-web-vulnerability-detection noobpk/gemini-web-vulnerability-detection:<version>`

`docker push noobpk/gemini-web-vulnerability-detection:<version>`

### Latest Version

`docker tag gemini-web-vulnerability-detection noobpk/gemini-web-vulnerability-detection:latest`

`docker push noobpk/gemini-web-vulnerability-detection:latest`
