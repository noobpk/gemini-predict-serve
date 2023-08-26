## Guide Build & Push Docker Image to Docker Hub

### Build Image

`docker build -t gemini-web-vuln-detection .`

### Tag and Push Image

`docker tag gemini-web-vuln-detection noobpk/gemini-web-vuln-detection:<version>`

`docker push noobpk/gemini-web-vuln-detection:<version>`

### Latest Version

`docker tag gemini-web-vuln-detection noobpk/gemini-web-vuln-detection:latest`

`docker push noobpk/gemini-web-vuln-detection:latest`