FROM ubuntu:latest

RUN mkdir URL_SHORTNER

COPY . URL_SHORTNER/

RUN 	apt-get update && apt install  python3-pip -y && \ 
	pip3 install -r URL_SHORTNER/requirements.txt


EXPOSE 8080

WORKDIR URL_SHORTNER

cmd ["python3","app.py"]
