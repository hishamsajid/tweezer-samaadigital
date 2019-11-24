import sys
sys.path.append('/home/hishamsajid/Documents/twitterapp/server/scripts')
print(sys.path)

from flask import Flask
from flask_restful import Resource,Api,reqparse
import pullInsert_tweets
import json


app = Flask(__name__)
api_rest = Api(app)



# class pullKey(Resource):
#     def get(self):
        
#         #set parameters to ask for
#         parser = reqparse.RequestParser()
#         parser.add_argument('term',type=str,help='Keyword or hashtag to search')
#         parser.add_argument('lang',type=str,help='language for which tweets are to be retrieved')
#         parser.add_argument('limit',type=int,help='number of tweets wanted, upper limit is 3200')
        
#         #unpack parameters into a dict
#         args = parser.parse_args()
        
#         #converts to json
#         result = pull_hashKey(term=args['term'],lang=args['lang'],limit=args['limit'])
#         result = json.dumps(result, indent=2, sort_keys=True, default=str)
        
#         return result

# ##ADD RESOURCE FOR PULLING A STREAM

# api_rest.add_resource(pullKey,'/keyOrTag')

# if __name__ == '__main__':
#     app.run(debug=True)