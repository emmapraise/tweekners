import GetOldTweets3 as got
import pandas as pd

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