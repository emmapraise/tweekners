from flask import Flask, render_template,url_for,request, redirect
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
import tweepy
import os
from datetime import date, timedelta

app = Flask(__name__)



consumer_key = 'PFhdQ6Sd4VaQyg9E3ffmsV12v'
consumer_secret = 'A8I4iiryzTgvt20tFVCPG5pay2iZYFYAx82Ligk8APFtVidayS'

# access_token = '2960988395-CxEU9JnTuF27RKdO2HJ1CCCco0slnZnDrWNUFIO'
# access_token_secret = 'DAYgUKakqBJWSNcjTVmt1ICzjpmNk1hMkQcJYdg4PQ8Lk'

app.config['SECRET_KEY'] = 'thisisthestart'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']  #'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

twitter_blueprint = make_twitter_blueprint(api_key=consumer_key, api_secret=consumer_secret, redirect_to= 'login')
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

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)

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

        query = User.query.filter_by(username=username)

        try:
            user= query.one()
        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        login_user(user)
    return redirect(url_for('user', name=account_info_json['screen_name']))

@app.route('/user', methods = ['GET', 'POST'])
def audit_user():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('user', name=username))

@app.route('/user/<string:name>')
@login_required
def user(name):
    usern = get_user(name)
    mytimeline = get_user_timeline(name)
    return render_template('loginuser.html', user=usern, user_time = mytimeline)

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))