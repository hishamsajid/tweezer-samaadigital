from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

tweets = [] 
class Listener(StreamListener):
    
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
            
        return(all_data['text'])
    
    def on_error(self,status):
        print(status)
