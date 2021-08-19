
import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import datetime
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
    print("*"*20)
    print("url :", url)
    if url in json_data.keys():
        return json_data[url]
    else:
        #creating random string for short url
        random_string = os.urandom(6)
        #converting the random string to hexadecimal
        short_str = random_string.hex().upper()
        check_data = {y:x for x,y in json_data.items()}
        while short_str in check_data.keys():
            random_string = os.urandom(6)
            short_str = random_string.hex().upper()
        #writing the shortend url to local file
        json_data[url] = short_str
        json_file = open('url.txt','w')
        json.dump(json_data, json_file)
        json_file.close()
        #returning the shortend url
        shorten_link = "http://127.0.0.1:8080/rd/"+short_str
        return shorten_link

#redirecting the short url to the original url
@app.route("/rd/<short_str>", methods=['GET'])
def url_redirect(short_str):
    '''
    Taking the Shorturl as input and redirecting to original url
    '''
    print("*"*20)
    print(short_str)
    #checking if the short url is present in the local file
    json_file = open('url.txt','r')
    json_data = json.load(json_file)
    json_file.close()

    #converting to (short url, long url) 
    json_data = {y:x for x,y in json_data.items()}
    if short_str in json_data.keys():
        #redirecting to the original url
        long_url = json_data[short_str]
        return redirect(long_url, code=302)
    else:
        #redirecting to the error page
        return redirect(url_for('error_page'), code=302)
    


# REST API to shorten the URL
@app.route('/short_url/', methods=['GET'])
def short_url(url='',method=None):
    '''
    url : long url sent as a request
    method: method for the type of  request

    This function is used as a REST API to convert long url to short url.
    '''
    # GET request
    try:
        if request.method == "GET":
            url = request.args.get('url')
    except:
        pass
    shorten_link = check_url(url)
    data = {"status" : "Success", "short_url":shorten_link}
    # returning the shortend url
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
        print("long_url :", long_url)
        #sending the request to shorten the url
        response = short_url(url=long_url,method="GET")
        
        #checking the status of the response
        data = json.loads(response.get_data().decode("utf-8"))
        if data['short_url']:
            return render_template('home.html', status=True, shortend_url=data['short_url'])
        else:
            return render_template('home.html', status=True, data=data['Remarks'])
    
    return render_template('home.html', status=status)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
