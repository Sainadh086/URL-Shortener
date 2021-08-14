import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests

app = Flask(__name__)

# REST API to shorten the URL
#@app.route('/short_url/<string:name>', methods=['GET'])

def short_url(url, method='GET'):
    api_key = os.environ['CUTTLY_API_KEY']
    headers = {"Authorization": api_key}
    # GET request
    if method == "GET":
        api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"
        #sending the post request to cuttly account for converting big url to shortend url
        shorten_response =  requests.get(api_url).json()["url"]
        
        # runs if the status is successfull
        if shorten_response["status"] == 7:
            shorten_link = shorten_response['shortLink']
            data = {"status" : "Success", "short_url":shorten_link}
            # returning the shortend url
            return data
        else:
            
            data = {"Status": "Failed", "Remarks" : "Check Credentials"}
            # return failed status
            return data

    # runs if get request is not used
    data = {"Status" : "Failed", "Remarks" : "Retry using GET Request" }
    return data


# a simple webpage to use the above rest api
@app.route("/", methods=['POST', 'GET'])
def web_page():
    status = False

    if request.method == 'POST':
        #getting long url from the webpage
        long_url = request.form.get('long_url')
        
        #loading the local url file, 
        json_file = open('url.txt','r')
        json_data = json.load(json_file)
        json_file.close()

        #to check the long url is already existing or not.

        if long_url in json_data.keys():
            shortend_url = json_data[long_url]
        else:
            response = short_url(long_url)
            shortend_url = response["short_url"]
            json_data[long_url] = shortend_url

            #writing the new url to the local file
            json_file = open('url.txt','w')
            json.dump(json_data, json_file)
            json_file.close()
        #json.dump(json_data, 'url.txt')
        return render_template('home.html', status=True, shortend_url=shortend_url)

    
    return render_template('home.html', status=status)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
