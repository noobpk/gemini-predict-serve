## Guide Build & Push Docker Image to Docker Hub

### Build Image

`docker build -t gemini-predit-serve .`

### Tag and Push Image

`docker tag gemini-predit-serve noobpk/gemini-predit-serve:<version>`

`docker push noobpk/gemini-predit-serve:<version>`

### Latest Version

`docker tag gemini-predit-serve noobpk/gemini-predit-serve:latest`

`docker push noobpk/gemini-predit-serve:latest`