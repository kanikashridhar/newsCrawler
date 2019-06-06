# Pipelines used in News Crawler are defined here.
#
# Pipelines defined here are added to ITEM_PIPELINES setting

from   scrapy.exceptions import DropItem
from   scrapy import signals
from   pydispatch import dispatcher
from   scrapy.exporters import JsonItemExporter
from   readability import Document
from   scrapy.conf import settings
from   datetime import datetime
from   lxml import etree
import requests, html2text
import pymongo, logging , os 

class NewsCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class NewsTextPipeline(object):
    '''
    DESCRIPTION:
    ------------
    This pipeline is used for extracting news article text.
    '''

    def process_item(self, item, spider):
        '''
        DESCRIPTION:
        ------------
        For each news item, corresponding news text is extracted
        using python library 'readability'.

        RETURNS:
        --------
        News item with 'newsText' field updated is returned.
        '''
        try:
            response = requests.get(item['newsUrl'])
            doc      = Document(response.text)
            content  = Document(doc.content()).summary()
            h = html2text.HTML2Text()
            h.ignore_links = True
            articleText    =  h.handle(content)
            articleText    =  articleText.replace('\r', ' ').replace('\n', ' ').strip()
            item['newsText'] = articleText
        except Exception:
            raise DropItem("Failed to extract article text from: " + item['newsUrl'])

        return item

class DropIfEmptyPipeline(object):
    '''
    DESCRIPTION:
    ------------
    This function drops news item if either of following
    mandatory fields are empty:
    1. newsHeadline
    2. newsUrl
    3. newsText
    
    '''
    def process_item(self, item, spider):
        if ((not item['newsHeadline']) or (not item['newsUrl'])
             or (not item['newsText']) ):
            raise DropItem()
        else:
            return item

class DuplicatesPipeline(object):
    '''
    DESCRIPTION:
    ------------
    This pipeline is used to remove the duplicate news items.
    '''
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['newsUrl'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['newsUrl'])
            return item

class MongoPipeline(object):
    '''
    DESCRIPTION:
    ------------
    * This pipeline is used to insert data in to MongoDB.
    '''
   
    def __init__(self, mongo_uri, mongo_db,mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        
    @classmethod
    def from_crawler(cls, crawler):
        mongo_user = os.environ.get('MONGOUSER', None)
        mongo_password = os.environ.get('MONGOPASSWD',None)
        
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI').format(user=mongo_user,password=mongo_password),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_collection= crawler.settings.get('MONGO_COLLECTION'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if ((data == 'newsUrl' or data == 'newsHeadline' or data == 'newsText') and not data):
                valid = False
                raise DropItem('News Item dropped, missing ' + data)
        if valid:
            logging.info("Going to insert Item"+ str(item))
            
            try:
                self.db[self.mongo_collection].insert(dict(item))
                logging.info('News Article inserted to MongoDB database!')
            except Exception as e :
                logging.info('Exception Occured while inserting data in MongoDB : '+str(e))

        return item

