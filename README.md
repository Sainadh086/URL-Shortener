# URL_SHORTNER

	Language used :- Python
	Built using :- Flask

## Container usage

	- docker run -itd --name short-url -p 8080:8080 sainadh086/url-shortner

## Rest API
	
	Sample usage
	- curl http://127.0.0.1:8080/short_url/?url=https://hub.docker.com/repository/docker/sainadh086/url-shortner
	
	Output
	- {
 		 "short_url": "http://127.0.0.1:8080/rd/4CED7520B4D8", 
  		 "status": "Success"
	  }


	Note:- Here I am using localhost, change the ip address according to your ip for redirecting.
