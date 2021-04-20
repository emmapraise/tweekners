from app.sentiment import to_Dataframe
from enum import unique
from flask import Flask, render_template,url_for,request, redirect
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from .gettweets import get_tweets_search, get_user,get_user_timeline
import os
from datetime import date, timedelta

app = Flask(__name__)

consumer_key = 'PFhdQ6Sd4VaQyg9E3ffmsV12v'
consumer_secret = 'A8I4iiryzTgvt20tFVCPG5pay2iZYFYAx82Ligk8APFtVidayS'

# access_token = '2960988395-CxEU9JnTuF27RKdO2HJ 1CCCco0slnZnDrWNUFIO'
# access_token_secret = 'DAYgUKakqBJWSNcjTVmt1ICzjpmNk1hMkQcJYdg4PQ8Lk'

app.config['SECRET_KEY'] = 'thisisthestart'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #os.environ['DATABASE_URL']  #
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


twitter_blueprint = make_twitter_blueprint(api_key=consumer_key, api_secret=consumer_secret, redirect_to= 'login')
app.register_blueprint(twitter_blueprint, url_prefix='/login')


current_date = date.today().isoformat() 
days_before = (date.today()-timedelta(days=30)).isoformat()


login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    user_name = db.Column(db.String(250))

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

@login_manager. user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


twitter_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user= current_user)

@app.route('/')
def home():
    myuser = get_user()
    mytimeline = get_user_timeline()
    return render_template('index.html', user = myuser,  user_time =mytimeline)

@app.route('/search')
def search():
    tweets = get_tweets_search()
    return render_template('search.html', tweets = tweets)

@app.route('/sentiment')
def sentiment():
    tweets = get_tweets_search()
    data = to_Dataframe(tweets)
    return render_template('sentiment.html', tweets = data)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    account_info = twitter.get('account/settings.json')
    account_info_json = account_info.json()
    return redirect(url_for('user', name=account_info_json['screen_name']))

@oauth_authorized.connect_via(twitter_blueprint)
def twitter_logged_in(blueprint, token):
    account_info = blueprint.session.get('account/settings.json')
    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json['screen_name']
        user_name = account_info_json['screen_name']#['name']

        query = User.query.filter_by(username=username)

        try:
            user= query.one()
        except NoResultFound:
            user = User(username=username, user_name = user_name)
            db.session.add(user)
            db.session.commit()

        login_user(user)
    return redirect(url_for('user', name=username))



@app.route('/search', methods = ['GET', 'POST'])
def audit_search():
    if request.method == 'POST':
        query = request.form['query']
        return redirect(url_for('getsearch', name=query))

@app.route('/search/<string:name>')
# @login_required
def getsearch(name):
    newtweets = get_tweets_search(name)
    return render_template('search.html', tweets = newtweets, name = name)

@app.route('/sentiment', methods = ['GET', 'POST'])
def audit_sentiment():
    if request.method == 'POST':
        query = request.form['query']
        return redirect(url_for('getsentiment', name=query))

@app.route('/sentiment/<string:name>')
# @login_required
def getsentiment(name):
    newtweets = get_tweets_search(name)
    data = to_Dataframe(newtweets)
    return render_template('sentiment.html', tweets = data, name = name)

@app.route('/user', methods = ['GET', 'POST'])
def audit_user():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('user', name=username))

@app.route('/user/<string:name>')
# @login_required
def user(name):
    usern = get_user(name)
    mytimeline = get_user_timeline(name)
    return render_template('index.html', user=usern, user_time = mytimeline, name = name)

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))