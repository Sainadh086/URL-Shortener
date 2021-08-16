
import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
from werkzeug.wrappers import response

app = Flask(__name__)


#checking the url present or not and sending request to cuttly api
def check_url(url):
    '''
    ulr: long url sent as a request

    This function takes the input from Web page and rest API. And converts the long url to short url.
    '''
    #loading the local url file, 
    json_file = open('url.txt','r')
    json_data = json.load(json_file)
    json_file.close()
    if url in json_data.keys():
        return json_data[url]
    else:
        #reading CUTTLY_API_KEY from environment variable
        api_key = os.environ['CUTTLY_API_KEY']
        api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"
        #sending the post request to cuttly account for converting big url to shortend url
        shorten_response =  requests.get(api_url).json()["url"]
        
        # runs if the status is successfull
        if shorten_response["status"] == 7:
            shorten_link = shorten_response['shortLink']
        #writing the shortend url to local file
        json_data[url] = shorten_link
        json_file = open('url.txt','w')
        json.dump(json_data, json_file)
        json_file.close()
        #returning the shortend url
        return shorten_link

# REST API to shorten the URL
@app.route('/short_url/', methods=['GET', 'POST'])
def short_url(url=None,method=None):
    '''
    url : long url sent as a request
    method: method for the type of  request

    This function is used as a REST API to convert long url to short url.
    '''
    # GET request
    if request.method == "GET" or method == "GET":
        url = request.args.get('url')
        shorten_link = check_url(url)
        data = {"status" : "Success", "short_url":shorten_link}
        # returning the shortend url
        return jsonify(data)

    # runs if get request is not used
    data = {"Status" : "Failed", "Remarks" : "Retry using GET Request" }
    return jsonify(data)


# a simple webpage to use the above rest api
@app.route("/", methods=['POST', 'GET'])
def web_page():
    '''
    Function is used to render the webpage and provide the required ouput.
    '''

    status = False

    if request.method == 'POST':
        #getting long url from the webpage
        long_url = request.form.get('long_url')

        #sending the request to shorten the url
        response = short_url(url=long_url,method="GET")
        
        #checking the status of the response
        data = json.loads(response.get_data().decode("utf-8"))
        if data['short_url']:
            return render_template('home.html', status=True, shortend_url=shortend_url)
        else:
            return render_template('home.html', status=True, data=data['Remarks'])
    
    return render_template('home.html', status=status)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
