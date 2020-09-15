from flask import Flask, render_template,url_for,request, redirect
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
import pandas as pd
import tweepy
import GetOldTweets3 as got
from datetime import date, timedelta

app = Flask(__name__)


consumer_key = 'PFhdQ6Sd4VaQyg9E3ffmsV12v'
consumer_secret = 'A8I4iiryzTgvt20tFVCPG5pay2iZYFYAx82Ligk8APFtVidayS'

access_token = '2960988395-CxEU9JnTuF27RKdO2HJ1CCCco0slnZnDrWNUFIO'
access_token_secret = 'DAYgUKakqBJWSNcjTVmt1ICzjpmNk1hMkQcJYdg4PQ8Lk'

twitter_blueprint = make_twitter_blueprint(api_key=consumer_key, api_secret=consumer_secret)
app.register_blueprint(twitter_blueprint, url_prefix='/login')

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

current_date = date.today().isoformat() 
days_before = (date.today()-timedelta(days=30)).isoformat()


def get_user(username = '_emmapraise'):
    user = api.get_user(username)
    return user

def get_user_timeline(username = '_emmapraise'):
    usertime = api.user_timeline(username)
    return usertime

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
    mytimeline = get_user_timeline()
    return render_template('index.html', user = myuser,  user_time =mytimeline)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    account_info = twitter.get('account/settings.json')

    if account_info.ok:
        account_info_json = account_info.json()
        return render_template('loginuser.html', user_log = account_info_json)
    
    return '<h1> Request Failed </h1>'
    # return render_template('logInUser.html')

@app.route('/user', methods = ['GET', 'POST'])
def audit_user():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('user', name=username))

@app.route('/user/<string:name>')
def user(name):
    usern = get_user(name)
    mytimeline = get_user_timeline(name)
    return render_template('index.html', user=usern, user_time = mytimeline)



