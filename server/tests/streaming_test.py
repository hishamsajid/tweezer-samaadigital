from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import os

with open('/home/hishamsajid/Documents/twitterapp/scripts/twitter_keys.json') as json_data:
    keys = json.load(json_data)

consumer_key = keys.get('consumer_key')
consumer_secret = keys.get('consumer_secret')
access_token = keys.get('access_token')
access_secret = keys.get('access_secret')

auth = OAuthHandler(consumer_key,consumer_secret)

auth.set_access_token(access_token,access_secret)
tweets = [] 

class listener(StreamListener):
    
    def on_data(self,data):
        
        all_data = json.loads(data)
        if 'text' in all_data:
            if(all_data['truncated']==True):
                print(all_data['extended_tweet']['full_text'])
                tweets.append(all_data['extended_tweet']['full_text'])
            else:
                print(all_data['text'])
                tweets.append(all_data['text'])
            
        print(len(tweets))
            
        return(True)
    
    def on_error(self,status):
        print(status)

twitterStream = Stream(auth = auth,listener = listener(),tweet_mode = 'extended')
twitterStream.filter(track=['car'])