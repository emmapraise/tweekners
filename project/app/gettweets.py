# import GetOldTweets3 as got
from datetime import date, timedelta
import tweepy

current_date = date.today().isoformat() 
days_before = (date.today()-timedelta(days=30)).isoformat()

consumer_key = 'PFhdQ6Sd4VaQyg9E3ffmsV12v'
consumer_secret = 'A8I4iiryzTgvt20tFVCPG5pay2iZYFYAx82Ligk8APFtVidayS'

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True) 

def get_user(username = '_emmapraise'):
    user = api.get_user(username)
    return user

def get_user_timeline(username = '_emmapraise'):
    usertime = api.user_timeline(username)
    return usertime


def get_tweets_search(query= 'EndSars',  max_tweet = 20):
    public_tweets = tweepy.Cursor(api.search, q= query, lang='en').items(max_tweet)
    return public_tweets 











# def get_tweets(username, top_only = True, start_date = current_date, end_date = days_before, max_tweets = 100):
#     """This function get User username and return their recent tweet for the last 30days
#     Input: 
#         Username: The username of the user. Default is _emmapraise
#         Top_only: set true to show the top tweets. Default is True
#         start_date = The day it should start getting the tweets from. Default is the current date.
#         end_date: The day it should stop getting the tweets. Default is 30 days before the current date.
#         max_tweets: The maximum number of tweets that should be generated. Default is set to 100.
#     """
#      # specifying tweet search criteria 
#     tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
#                           .setTopTweets(top_only)\
#                           .setSince(start_date)\
#                           .setUntil(end_date)\
#                           .setMaxTweets(max_tweets)
    
#     # scraping tweets based on criteria
#     tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    
#     # creating list of tweets with the tweet attributes 
#     # specified in the list comprehension
#     text_tweets = [[tw.username,
#                 tw.text,
#                 tw.date,
#                 tw.retweets,
#                 tw.permalink,
#                 tw.mentions,
#                 tw.hashtags] for tw in tweet]
    
#     # creating dataframe, assigning column names to list of
#     # tweets corresponding to tweet attributes
#     news_df = pd.DataFrame(text_tweets, 
#                             columns = ['User', 'Text','Date', 'URL' 'Retweets', 'Mentions', 'HashTags'])
    
#     return news_df


