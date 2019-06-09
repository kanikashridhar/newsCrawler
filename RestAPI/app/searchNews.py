# News Search Rest API

from   flask import Flask,jsonify,request
from   flask_restful import Resource, Api
from   flask_pymongo import PyMongo
import os 
from   bson import json_util
import json

# Connecting to MongoDB containing the crawled BBC News Articles.
app    = Flask(__name__)


mongo_user = os.environ.get('MONGOUSER', None)
mongo_password = os.environ.get('MONGOPASSWD',None)
mongo_uri = 'mongodb://{user}:{password}@ds231537.mlab.com:31537/newsarticles'
mongo_uri.format(user=mongo_user,password=mongo_password)


app.config['MONGO_URI']    =  mongo_uri.format(user=mongo_user,password=mongo_password)
app.config['MONGO_DBNAME'] = 'newsarticles'

api         = Api(app)
mongo       = PyMongo(app)
collection  = mongo.db.news


collection.create_index([
           ('newsHeadline', 'text'),
           ('newsText', 'text'),
        ],
       
        name="search_index",
        weights={
           'newsText':10,
           'newsHeadline':25
         }
       )


class news(Resource):  

   def get(self):
      '''
        DESCRIPTION:
        ------------
        GET news articles, where keyword appears in news article text.

        PARAMETERS:
        ----------
        1. keyword: string to be searched in news text.
      '''
      page_size = 10
      try:
         page_num = int(request.args.get("page"))
      except:
         page_num = 1

      try:
         keyword = request.args.get("searchkey",None)            
      except:
         return jsonify({'result':'Please Enter a valid Keyword'})
      
      skips = page_size * (page_num - 1)
      nextPage = page_num + 1

      if keyword:
         text_results = collection.find({"$text": {"$search": keyword}}).skip(skips).limit(page_size)
      else:  
         text_results = collection.find().skip(skips).limit(page_size)

      json_results = []

      for result in text_results:
            json_results.append(
                                  { 
                                    'author'      : result['author'], 
                                    'Title'       : result['newsHeadline'], 
                                    'Link'        : result['newsUrl'],
                                    'article text': result['newsText']
                                  }
                                )
     
      #if no more records are left to be displayed, set the nextPage as 1
      if text_results.count(True) < page_size:
         nextPage=1

      return jsonify({'nextPage':nextPage,'result' : json_results})

api.add_resource(news, '/news')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
