import sys
import json
import tweepy
import pandas as pd
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
tweets = pd.DataFrame()
dd = pd.DataFrame()
class TweetListener (StreamListener) :
    def __init__ (self):
        pass
    def on_data (self,data):
            try :
#                print(data)
                jsonMessage = json.loads(data)
                print(jsonMessage)
            except KeyError as e:
                print ("KeyError on_data : %s" % str(e))
            return True
    def on_error (self, status):
        print(status)
        return True

if __name__ == "__main__":
        api_key = "83jIXVzuM6fiuWTWuROCNlr0u"
        api_secret = "xmUTHxEBiDpAgEMZBXqly90Na56AvPz3XiJAV9dfc3HYqHaY2L"
        access_token = "149166933-E24MXLzA4bpPVCxzTtbc6TwEXddhjQTtRj00HeZ0"
        access_token_secret = "YWl6yoB81OLBkBbxPo5cqlZtLbw0jkKd8guypbxVcUU7H"
        auth = OAuthHandler (api_key, api_secret)
        auth.set_access_token(access_token,access_token_secret)
        twitter_stream = Stream(auth, TweetListener())
        twitter_stream.filter(track=['#python'])
