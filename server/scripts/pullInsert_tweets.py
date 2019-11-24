from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime
import json
from streamer import Listener
from streamer import StreamListener
from streamer import Stream
from flask import Flask
from flask_restful import Resource,Api,reqparse
from flask_cors import CORS, cross_origin


with open('twitter_keys.json') as json_data:
    keys = json.load(json_data)

consumer_key = keys.get('consumer_key')
consumer_secret = keys.get('consumer_secret')
access_token = keys.get('access_token')
access_secret = keys.get('access_secret')

auth = OAuthHandler(consumer_key,consumer_secret)

auth.set_access_token(access_token,access_secret)

api = API(auth)
app = Flask(__name__)
CORS(app)
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api_rest = Api(app)



def pull_tweets_user(userId,limit):
    """
    pulls users tweet using Twitter ID (userId), has a limit of up to 3200
    """


    for tweet in Cursor(api.user_timeline, id = userId,tweet_mode='extended').items(limit=limit):
        

        tweet_json = {

        'user_name': tweet.user.screen_name,
        'tweet_text': tweet.full_text,
        'location': tweet.user.location,
        'created_at': tweet.created_at,
        'favourites_count': tweet.favorite_count,
        'retweets':tweet.retweet_count,
        'followers_count': tweet.user.followers_count,
        'verified': tweet.user.verified,
        '_id': tweet.id
        }

        print(tweet_json)


def pull_hashKey(term,lang,limit):
    """
    pulls Tweets using a keyword or Hashtag. Will get username, location, timezone, date and time created
    number of times favourited, number of followers the tweeter has. \n For now the limit is 3200.
    """
    tweet_dict = []
    for tweet in Cursor(api.search, q = term, lang = lang).items(limit):
        
        if(lang != 'en'):
            print('Language not supported, please contact dev')
            break

        tweet_json = {

        'user_name': tweet.user.screen_name,
        'tweet_text': tweet.text,
        'location': tweet.user.location,
        'created_at': str(tweet.created_at),
        'favourites_count': tweet.favorite_count,
        'retweets':tweet.retweet_count,
        'followers_count': tweet.user.followers_count,
        'verified': tweet.user.verified,
        '_id': tweet.id
        }
        print(tweet_json)
        tweet_dict.append(tweet_json)
    return tweet_dict

def pull_Semistream():
    """
    pulls semi-streaming data related to #tag or keyword
    """
    pass


def pull_stream(term):
    twitterStream = Stream(auth = auth,listener = Listener(),tweet_mode = 'extended')
    return twitterStream.filter(track=[term])



#API resource request for using keyword or hasthag
class pullKey(Resource):
    def get(self):
        
        #set parameters to ask for
        parser = reqparse.RequestParser()
        parser.add_argument('term',type=str,help='Keyword or hashtag to search')
        parser.add_argument('lang',type=str,help='language for which tweets are to be retrieved')
        parser.add_argument('limit',type=int,help='number of tweets wanted, upper limit is 3200')
        
        #unpack parameters into a dict
        args = parser.parse_args()
        print(args)
        #converts to json
        result = pull_hashKey(term=args['term'],lang=args['lang'],limit=args['limit'])
        # result = pull_hashKey(term=args['term'],lang='en',limit=20)
        
        #result = json.dump(result)
        
        return result

##ADD RESOURCE FOR PULLING A STREAM

class getStream(Resource):
    
    def get(self):
        
        parser =reqparse.RequestParser()
        parser.add_argument('term',type=str,help='Keyword or hashtag to search')
        args = parser.parse_args()
        result = pull_stream(args['term'])
        result = json.dumps(result, indent=2, sort_keys=True, default=str)

        return result

        


api_rest.add_resource(pullKey,'/api/keyOrTag')
api_rest.add_resource(getStream,'/api/stream')

if __name__ == '__main__':
    app.run(debug=True)
