# News Search Rest API

from   flask import Flask,jsonify,request
from   flask_restful import Resource, Api
from   flask_pymongo import PyMongo
import os 
from   bson import json_util
import json

# Connecting to MongoDB containing the crawled BBC News Articles.
app    = Flask(__name__)
app.config['MONGO_DBNAME'] = 'newsarticles'

mongo_user = os.environ.get('MONGOUSER', None)
mongo_password = os.environ.get('MONGOPASSWD',None)

print("mongo_password "+ str(mongo_password))
mongo_uri = 'mongodb://{user}:{password}@ds231537.mlab.com:31537/newsarticles'


app.config['MONGO_URI']    = mongo_uri.format(user=mongo_user,password=mongo_password)
print("mongo_uri"+ str(app.config['MONGO_URI']))

#mongo_collection = 'news'

api         = Api(app)
mongo       = PyMongo(app)
collection  = mongo.db.news
print("mongo collection"+ str(collection))


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
    #def json(self):
    #    return {'name':self.name,'price':self.price,'store_id':self.store_id}
    

    def get(self, keyword):
        '''
        DESCRIPTION:
        ------------
        GET news articles, where keyword appears in news article text.

        PARAMETERS:
        ----------
        1. keyword: string to be searched in news text.
        '''
        PAGE_SIZE = 5
        try:
           page = int(request.args.get("page"))
        except:
           page = 0

        start = page * PAGE_SIZE
        end = (page + 1) * PAGE_SIZE
        text_results = collection.find({"$text": {"$search": keyword}}).limit(end)
       
        print("start is"+str(start)+" and end is: "+str(end))
        totalRecords = text_results.count()
        if (totalRecords < end):
            end = totalRecords
        
        if (totalRecords<start):
            start = totalRecords-1

        doc_matches = text_results[start:end]

        json_results = []
        for result in doc_matches:
            output = []
            json_results.append(
                                {'author'      : result['author'], 
                                 'Title'       : result['newsHeadline'], 
                                 'Link'        : result['newsUrl'],
                                 'article text': result['newsText']
                                }
                                )
 
        return jsonify({'result' : json_results})


api.add_resource(news, '/news/<string:keyword>')

if __name__ == '__main__':
    app.run(debug=True)