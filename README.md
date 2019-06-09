# News Website Crawler
Crawler using Scrapy + Readability + MongoDB (to store documents)


    The newscrawler Application
    1. Crawling:- Crawls news website using the SCRAPY crawler framework (http://scrapy.org/).

    2. Cleaning:- Cleanse the articles using Readbility framework to obtain only information relevant to the news story, e.g. article text, author, headline and article url. 

    3. Database:- News articles crawled are stored in Mongo Database hosted at mLab (https://mlab.com/) for subsequent search and retrieval.

    4. API:- RestAPI is provided to access the content in the mongo database using a keyword search for the articles. 
    [Text index has been created on headline and article text fields to expedite the search process]

    5. Pagination:- Five articles will be returned on each search page. User can specify the page number in the search URL.


# how to run the spider
* Install Python 3.x if not already
* Create and activate virtual env
```
python3 -m venv venv
source venv/bin/activate
```

* Now install the crawler requirements
```
cd newsCrawler
pip install -r requirements.txt
```
* exporting DB credentials
```
export MONGOUSER=<user>
export MONGOPASSWD=<passwd>
```

* Run the scrapy crawler

```
scrapy crawl crawler filename=rules.json

The command will take long (in hours). It is advisable to execute the command in background.
Meanwhile user can see the Logs in Log folder to check the progress of the spider execution.
A "visited_urls.txt" which is dynamically created in Output folder, represents already scraped URLs. The purpose of this file is to avoid scraping same pages.

```
* Explaining rules.json file
Rules for crawling are defined in this file. User can choose the file name of his choice and can edit the file as per the crawling requirements.

```
a) "allowed_domains" : ["bbc.com"],
     Domains allowed to be scraped.


b) "start_urls": [
		"https://www.bbc.com/sport/cricket"
	],

    The starting URL of the website.

c) "rules": [
		{
			"allow": ["https://www.bbc.com/sport/cricket"],
			"follow": true,
			"callback": "parseItems"
		}
	],
    
Here, User can specify which all links are allowed to be scraped. A "deny" parameter similar to allow can be used to specify which all links need to be removed from the scraping list.

d) "paths": {
   "title" : [
		   ".//div[@id='responsive-story-page']/article/h1[@class='story-headline gel-trafalgar-bold ']/text()",
		   "//title/text()"
		  ],
	"author" : [
		    ".//div[@class='gel-flag__body']/p[@class='gel-long-primer']/text()"
                   ]
	}

Paths defines the xpath configurations to be used to fetch the author and title information from the scraped page.
```

# Executing RestAPI
## Option-1 Without docker

* Install Python 3.x if not already
* Create and activate virtual env if not already created

```
python3 -m venv venv
source venv/bin/activate
```

* Installing API Requirements 
```
cd RestAPI
pip install -r requirements.txt
```

* exporting DB credentials
```
export MONGOUSER=<user>
export MONGOPASSWD=<passwd>
```

* Run the api 
```
python app/searchNews.py

```

* The API can be accessed at

```
[http://localhost:5000/news?searchkey=keyword&page=page_number ](http://127.0.0.1:5000/news?searchkey=keyword&page=page_number)


Replace "keyword" with the actual keyword to be searched in the database.
Replace "page_number" is a integer page number value.By default, the page num is 1. A maximum of 5 articles can be seen on each page.

```
## Option-2  Using Docker

* cd localdir

```
cd RestApi
```

* Build the docker image
```
docker build -t newsapi:v1.0 .
``` 

* Run the docker image
```
docker run --env MONGOUSER=<username>  --env MONGOPASSWD=<password> -p 5000:5000 newsapi:v1.0
```

This will start the server and you can access the API by browsing to [http://localhost:5000/news?searchkey=keyword&page=page_number ](http://127.0.0.1:8000/news/<keyword>?page=<page_num>)

Replace "keyword" with the actual keyword to be searched in the database.
Replace "page_number" is a integer page number value.By default, the page num is 1. A maximum of 5 articles can be seen on each page.