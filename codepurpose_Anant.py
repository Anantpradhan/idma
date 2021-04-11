import json
import pandas as pd
import datetime
from datetime import datetime
import  numpy as np
import glob
import seaborn as sns
import matplotlib.pyplot as plt

#Define a function to check the word in tweet
def check_word_in_tweet(word, data):
    """Checks if a word is in a Twitter dataset's text.
    Checks text and extended tweet (140+ character tweets) for tweets,
    retweets and quoted tweets.
    Returns a logical pandas Series.
    """
    contains_column = data['text'].str.contains(word, case = False)
    contains_column |= data['extended_tweet-full_text'].str.contains(word, case = False)
    contains_column |= data['quoted_status-text'].str.contains(word, case = False)
    contains_column |= data['retweeted_status-text'].str.contains(word, case = False)
    return contains_column

tweets_data = []
tweets_file = open(tweets_data_path,encoding="utf8" )
tweets = []
files  = list(glob.iglob( "C:\\Users\\Achyut\\Desktop\\test\\twitter_data.json"))
for f in files:
    fh = open(f, 'r', encoding='utf-8' )
    tweets_json = fh.read().split("\n")
    print (tweets_json)
## remove empty lines from the tweets
    tweets_json = list(filter(len, tweets_json))
    for tweet in tweets_json:
        try:
            tweet_obj = json.loads(tweet).encode('utf-8')  # Gettting Decode error here , need to resolve
        except JSONDecodeError as e:
            print ("Decoder Error")
        except TypeError as e:
            print("TypeError")

        # Store the user screen name in 'user-screen_name'
        tweet_obj['user-screen_name'] = tweet_obj['user']['screen_name']
        tweets.append(tweet_obj)
        if 'retweeted_status' in tweet_obj:
            # Store the retweet user screen name in 'retweeted_status-user-screen_name'
            tweet_obj['retweeted_status-user-screen_name'] = tweet_obj['retweeted_status']['user']['screen_name']
            # Store the retweet text in 'retweeted_status-text'
            tweet_obj['retweeted_status-text'] = tweet_obj['retweeted_status']['text']
# Convert tweet to Dataframe
df_tweet = pd.DataFrame(tweets)

# Find mentions of #python in all text fields
python = check_word_in_tweet('python', df_tweet)
# Find mentions of #javascript in all text fields
js = check_word_in_tweet('javascript', df_tweet)

# Print proportion of tweets mentioning #python
print("Proportion of #python tweets:", np.sum(python) / df_tweet.shape[0])

# Print proportion of tweets mentioning #rstats
print("Proportion of #javascript tweets:", np.sum(js) / df_tweet.shape[0])

# Print created_at to see the original format of datetime in Twitter data
print(df_tweet['created_at'].head())

# Convert the created_at column to np.datetime object
df_tweet['created_at'] = pd.to_datetime(df_tweet['created_at'])

# Print created_at to see new format
print(df_tweet['created_at'].head())

# Set the index of df_tweet to created_at
df_tweet = df_tweet.set_index('created_at')

# Create a python column
df_tweet['python'] = check_word_in_tweet('python', df_tweet)

# Create an js column
df_tweet['js'] = check_word_in_tweet('javascript', df_tweet)


# Average of python column by day
mean_python = df_tweet['python'].resample('1 min').mean()

# Average of js column by day
mean_js = df_tweet['js'].resample('1 min').mean()

# Plot mean python/js by day
plt.plot(mean_python.index.minute, mean_python, color = 'green')
plt.plot(mean_js.index.minute, mean_js, color = 'blue')

# Add labels and show
plt.xlabel('Minute'); plt.ylabel('Frequency')
plt.title('Language mentions over time')
plt.legend(('#python', '#js'))
plt.show()


