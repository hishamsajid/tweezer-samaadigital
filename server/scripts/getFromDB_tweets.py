from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import pandas as pn
import simplejson
import datetime
from datetime import datetime, date, time, timedelta
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client['test-db']

def get_tweets(collection_name):
    
  
    
    twitter_user = db[collection_name]
    #print(twitter_user)

    cursor = twitter_user.find({})
    #print(cursor[50])
    user_name = []
    tweet_text = []
    created_at = []
    location = []
    favourites_count = []
    retweets = []
    followers_count = []


    for item in cursor:
        
        #print(item['user_name'])
        user_name.append(item['user_name'])
        tweet_text.append(item['tweet_text'])
        created_at.append(item['created_at'])
        location.append(item['location'])
        favourites_count.append(item['favourites_count'])
        retweets.append(item['retweets'])
        followers_count.append(item['followers_count'])
        


    df = pn.DataFrame({
        'user_name': user_name,
        'tweet_text': tweet_text,
        'created_at': created_at,
        'location': location,
        'favourites_count':favourites_count,
        'retweets': retweets,
        'followers_count': followers_count
    })

    df_sorted = df.sort_values(by='created_at',ascending=False)
    #print(df_sorted)
    return df_sorted
