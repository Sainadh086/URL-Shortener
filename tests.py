# A simple unit test for the functions in the module.

#importing packages
import json
import requests
from werkzeug.wrappers import response

# sending a request to the server
def send(url):
    try:
        #channge the request api of the server, accordingly
        response = requests.get(f'http://127.0.0.1:8080/short_url/?url={url}')
        #reading the response
    except:
        return "Error"
    return response.json()


# sending request in wrong format
def test_wrong_url(url):
    response = requests.post(url='http://127.0.0.1:8080/short_url/', data={'url':url})
    return response.text

if __name__ == '__main__':
    long_url =  'https://hub.docker.com/repository/docker/sainadh086/url-shortner'
    print(test_wrong_url(long_url))
    print(send(long_url))
    
