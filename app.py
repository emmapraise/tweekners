from flask import Flask, render_template,url_for,request, redirect
import pandas as pd
import tweepy
import GetOldTweets3 as got
from datetime import date, timedelta

consumer_key = '4UVqA44fSYOp1zeFGfsCVuZWf'
consumer_secret = 'eccY5JdQxZOa2uOqaCVguvuhePFBMdXWGpu0hMqpWKmkcO1Qjc'

access_token = '2960988395-EfALUKwhVrslW0vm6fmGwEKIu0Elv9IRR8IjF08'
access_token_secret = 'FH0j7w0Iiqjh35Ek24h0UFUSiWPUeAi3HqCmTDpDHMyhr'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

current_date = date.today().isoformat() 
days_before = (date.today()-timedelta(days=30)).isoformat()


def get_user(username = '_emmapraise'):
    user = api.get_user(username)
    return user

    
def get_tweets(username, top_only = True, start_date = current_date, end_date = days_before, max_tweets = 100):
    """This function get User username and return their recent tweet for the last 30days
    Input: 
        Username: The username of the user. Default is _emmapraise
        Top_only: set true to show the top tweets. Default is True
        start_date = The day it should start getting the tweets from. Default is the current date.
        end_date: The day it should stop getting the tweets. Default is 30 days before the current date.
        max_tweets: The maximum number of tweets that should be generated. Default is set to 100.
    """
     # specifying tweet search criteria 
    tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                          .setTopTweets(top_only)\
                          .setSince(start_date)\
                          .setUntil(end_date)\
                          .setMaxTweets(max_tweets)
    
    # scraping tweets based on criteria
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    
    # creating list of tweets with the tweet attributes 
    # specified in the list comprehension
    text_tweets = [[tw.username,
                tw.text,
                tw.date,
                tw.retweets,
                tw.permalink,
                tw.mentions,
                tw.hashtags] for tw in tweet]
    
    # creating dataframe, assigning column names to list of
    # tweets corresponding to tweet attributes
    news_df = pd.DataFrame(text_tweets, 
                            columns = ['User', 'Text','Date', 'URL' 'Retweets', 'Mentions', 'HashTags'])
    
    return news_df

app = Flask(__name__)

def get_tweets_search(state, startdate, enddate, maxtweet):
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch("Flood")\
                                            .setSince(startdate)\
                                            .setUntil(enddate)\
                                            .setNear(state)\
                                            .setWithin("500mi")\
                                            .setMaxTweets(maxtweet)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    
    text_tweets = [[tw.username,
                tw.text,
                tw.date,
                tw.retweets,
                tw.favorites,
                tw.mentions,
                tw.hashtags,
                tw.geo] for tw in tweet]
    df_state= pd.DataFrame(text_tweets, columns = ['User', 'Text', 'Date', 'Favorites', 'Retweets', 'Mentions','Hashtags', 'Geolocation'])
    
    return df_state

# df_1 = get_tweets_search('Wisconsin', "2019-07-18", "2019-07-20", 1000)
# print(df_1.head())


# Defining news sources I want to include
news_sources = ['nytimes', 'bbcbreaking', 'bbcnews', 'bbcworld', 'theeconomist', 'reuters','wsj', 'financialtimes', 'guardian']
# getting tweets from the defined new sources, 
# only including top tweets, 
# looking at the past week with the end_date not inclusive,
# and specifying that we want a max number of tweets = 100.
# also sorting the tweets by date, descending.

# news_df = get_tweets(news_sources, 
#                      top_only = True,
#                      start_date = "2020-04-07", 
#                      end_date = "2020-04-14",
#                     max_tweets = 100).sort_values('Date',         ascending=False)
# print(news_df.head())

@app.route('/')
def home():
    myuser = get_user()
    return render_template('index.html', user= myuser)

@app.route('/user', methods = ['GET', 'POST'])
def audit_user():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('user', name=username))

@app.route('/user/<string:name>')
def user(name):
    usern = get_user(name)
    return render_template('index.html', user=usern)


if __name__ == '__main__':
	app.run(debug=True)
