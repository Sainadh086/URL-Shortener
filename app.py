
import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
from werkzeug.wrappers import response

app = Flask(__name__)

class json_check():
    def __init__(self):
        self.json_file = open("url.txt",'r')
        self.json_data = json.load(self.json_file)
        self.json_data_reverse = {v: k for k, v in self.json_data.items()}
        self.json_file.close()
    def get_url_status(self, url):
        if self.json_data.get(url):
            short_str = self.json_data[url]
        else:
            random_string = os.urandom(6)
            short_str = random_string.hex().upper()
            while self.json_data_reverse.get(short_str):
                random_string = os.urandom(6)
                short_str = random_string.hex().upper()
            self.update_json(url,short_str)
        shorten_link = "http://127.0.0.1:8080/rd/"+short_str
        return shorten_link
    def get_original_url(self, short_str):
        if self.json_data_reverse.get(short_str):
            return self.json_data_reverse[short_str]
        else:
            return False
    def update_json(self,url,short_str):
        self.json_data[url] = short_str
        self.json_data_reverse[short_str] = url
        json_file = open("url.txt",'w')
        json.dump(self.json_data,json_file)
        self.json_file.close()

check_obj = json_check()


#checking the url present or not and sending request to cuttly api
def check_url(url):
    #returning the shortend url
    short_str = check_obj.get_url_status(url)
    shorten_link = "http://127.0.0.1:8080/rd/"+short_str
    return shorten_link

#redirecting the short url to the original url
@app.route("/rd/<short_str>", methods=['GET'])
def url_redirect(short_str):
    '''
    Taking the Shorturl as input and redirecting to original url
    '''  
    long_url = check_obj.get_original_url(short_str)

    if long_url:
        return  redirect(long_url, code=302)  
    else:
        return "<h1> ERROR 404 URL NOT FOUND <h1>"
    


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
            #header = request.headers
            #if header['Content-Type'] == 'application/json':
                url = request.args.get('url')
        else:
            return jsonify({"error":"Method type must be GET"})
    except:
        pass
    shorten_link = check_obj.get_url_status(url)
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
    app.run(host="0.0.0.0", port=8080, debug=False)
