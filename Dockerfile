FROM ubuntu:latest

RUN mkdir URL_SHORTNER

COPY . URL_SHORTNER/

RUN 	apt-get update && apt install  python3-pip -y && \ 
	pip3 install -r URL_SHORTNER/requirements.txt


EXPOSE 8080

cmd ["python3","URL_SHORTNER/app.py"]
