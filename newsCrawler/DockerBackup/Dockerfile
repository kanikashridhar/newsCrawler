FROM python:3.7

WORKDIR /scrapycrawler

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY /news_crawler/ ./news_crawler/
COPY scrapy.cfg .
COPY rules.json .

CMD ["scrapy", "crawl", "crawler","-a","filename=rules.json"]
