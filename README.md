# gemini-predict-serve
A predict serve for gemini-self-protector

## Deploy Predict Serve with Docker

To deploy predict serve using docker, follow these steps -

1. Download this `docker-compose.yml` on your local machine or any other system where you have installed Docker. Replace `your-auth-key` with whatever you want. Suggest to use `uuid` or `sha256` for this key.

```
$ wget -O docker-compose.yml https://raw.githubusercontent.com/noobpk/gemini-self-protector/dev/predict-server/docker-compose.yml
```
2. Open terminal in that directory

3. Run following command to run container

```
$ docker-compose up
```