# News Search Rest API

from   flask import Flask,jsonify
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
        #results = mongo.db.news.find({'newsText': {'$regex': '.*' + keyword + '.*'}})
        results = collection.find({"$text": {"$search": keyword}}).limit(10)
        json_results = []
        for result in results:
            print ("result is "+str(result))
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