## Guide Build & Push Docker Image to Docker Hub

### Build Image

`docker build -t gemini-predict-serve .`

### Tag and Push Image

`docker tag gemini-predict-serve noobpk/gemini-predict-serve:<version>`

`docker push noobpk/gemini-predict-serve:<version>`

### Latest Version

`docker tag gemini-predict-serve noobpk/gemini-predict-serve:latest`

`docker push noobpk/gemini-predict-serve:latest`