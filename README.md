# News Website Crawler
Crawler using Scrapy + Readability + MongoDB (to store documents)

The newscrawler Application performs the following functions:

1. Crawling:- Crawls the given news website using the [Scrapy crawler framework](http://scrapy.org/).

2. Cleaning:- Cleanse the articles using Readbility framework to obtain only information relevant to the news story, e.g. article text, author, headline and article url. 

3. Database:- News articles crawled are stored in Mongo Database hosted at [mLab](https://mlab.com/) for subsequent search and retrieval.

4. API:- A minimal REST API is created using Flask to access the content in the mongo database using a keyword search for the articles. Have created a Text index on headline and article text fields to expedite the search process.

5. Pagination:- Ten articles will be returned on each search page. User can specify the page number in the search URL.

# How to run the spider
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
scrapy crawl crawler -a filename=rules.json
```

The crawler typically takes a long time to crawl the website - depends on the site and the pages available to crawl.
Meanwhile user can see the Logs in Log folder to check the progress of the spider execution.
Another file is created in the output folder -  "visited_urls.txt" which tracks the already scraped URLs. The purpose of this file is to avoid scraping same pages again.


rules.json - 
Rules for crawling the website or part of it are defined in this file. User can choose the file name of his choice and can edit the file as per the crawling requirements. Given is just an example where our crawler crawls the BBC website and specifically the sports-cricket section of it. The rules defines XPath queries to fetch the author and title information from the scraped page.

# REST API 

Following APIs are provided: 

1. Get All news articles ( paginated by default ) - [http://localhost:5000/news](http://localhost:5000/news)

* An optional parameter "page" can be used to fetch the next page of the articles. The next page number is specified in the response


2. Search news articles by keyword -  [http://localhost:5000/news?searchkey=keyword&page=page_number](http://localhost:5000/news?searchkey=keyword&page=page_number)

* Replace "keyword" with the actual keyword to be searched in the database.
* Replace "page_number" with an integer value. A maximum page size of 10 articles is kept currently, which can be made configurable easily. 

# Building & Deploying REST API
## Option 1 - Without docker

* Install Python 3.x if not already
* Create and activate virtual env if not already done

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

## Option 2 - Using Docker

* Build the docker image after going into the RestAPI directory
```
docker build -t newsapi:v1.0 .
``` 

* Run the docker image
```
docker run --env MONGOUSER=<username>  --env MONGOPASSWD=<password> -p 5000:5000 newsapi:v1.0
```

This will start the server and you can access the above mentioned API
