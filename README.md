# URL_SHORTNER

	Language used :- Python
	Built using :- Flask

## Cuttly Account

Generating the shortend api using Cuttly services. To get the Cuttly api key create an account <a href ="https://cuttly/register" >click_here</a>

## Container usage

	- docker run -itd --name short-url -p 8080:8080 -e CUTTLY_API_KEY="<your_api_key>" sainadh086/url-shortner

## Rest API
	
	Sample usage
	- curl http://127.0.0.1:8080/short_url/?url=https://hub.docker.com/repository/docker/sainadh086/url-shortner
	
	Output
	- {
 		 "short_url": "https://cutt.ly/oQK2mqt", 
  		 "status": "Success"
	  }

