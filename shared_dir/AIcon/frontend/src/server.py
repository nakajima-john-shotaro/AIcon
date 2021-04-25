import argparse
from logging import NOTSET
from os import pardir
from flask import Flask, jsonify, redirect, session, render_template, request
from flask.helpers import make_response
from flask_cors import CORS
import urllib.parse

import tweepy

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["JSON_AS_ASCII"] = False

consumer_key_twitter: str = None
consumer_secret_twitter: str = None
access_token_twitter: str = None
access_token_secret_twitter: str = None

url = "https://api.twitter.com/1.1/account/update_profile_image.json?user_id="

CORS(app)

@app.route("/")
def index():
    return render_template("index.html", title="AIcon", name="AIcon")


@app.route("/twitter-auth", methods=["POST"])
def twitter():
    print(f"Twitter CONSUMER_KEY: {consumer_key_twitter}")
    print(f"Twitter CONSUMER_SECRET: {consumer_secret_twitter}")
    print(f"Twitter ACCESS_TOKEN: {access_token_twitter}")
    print(f"Twitter ACCESS_TOKEN_SECRET: {access_token_secret_twitter}")

    s_data = {}

    twitter_auth = tweepy.OAuthHandler(consumer_key=consumer_key_twitter, consumer_secret=consumer_secret_twitter)

    try:
        s_data['auth_url'] = twitter_auth.get_authorization_url()
        print(session)
    except tweepy.TweepError as e:
        print(e)
        s_data['auth_url'] = ""
    print(s_data['auth_url'])
    response = make_response(jsonify(s_data))
    return response

@app.route("/twitter")#, methods=["GET"])
def twitter_callback():
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    return render_template("twitter-callback.html", oauth_token=oauth_token, oauth_verifier=oauth_verifier)

@app.route("/twitter-send")#, methods=["GET"])
def twitter_send():
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    print('oauth_token:', oauth_token)
    print('oauth_verifier:', oauth_verifier)

    twitter_auth = tweepy.OAuthHandler(consumer_key_twitter, consumer_secret_twitter)
    twitter_auth.request_token = {
        'oauth_token': oauth_token,
        'oauth_token_secret': oauth_verifier
    }

    try:
        twitter_auth.get_access_token(oauth_verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    img_path = request.cookies.get('img_path')
    mode = request.cookies.get('twitter_mode')

    api = tweepy.API(auth_handler=twitter_auth)
        
    if mode == 'icon':
        img_path = urllib.parse.unquote(img_path)
        try:
            api.update_profile_image(img_path)
            print('Twitter: Success')
        except tweepy.TweepError as e:
            print(e)
            print('Twitter: Failed')
    elif mode == 'tweet':
        img_path = urllib.parse.unquote(img_path)
        api.update_with_media(status="AIconでアイコンを作ったよ！！\n#ハッカソン\n#技育CAMP\n#新しいプロフィール画像", filename=img_path)

    return render_template("twitter-send.html", title="Twitter-Send", name="Twitter-Send")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--consumer-key",
        type=str,
        metavar="CONSUMER_KEY",
        help="CONSUMER_KEY for Twitter",
    )
    parser.add_argument(
        "-C",
        "--consumer-secret",
        type=str,
        metavar="CONSUMER_SECRET",
        help="CONSUMER_SECRET for Twitter",
    )
    parser.add_argument(
        "-t",
        "--access-token",
        type=str,
        metavar="ACCESS_TOKEN",
        help="ACCESS_TOKEN for Twitter",
    )
    parser.add_argument(
        "-s",
        "--access-token-secret",
        type=str,
        metavar="ACCESS_TOKEN_SECRET",
        help="ACCESS_TOKEN_SECRET for Twitter",
    )

    args = parser.parse_args()

    consumer_key_twitter = args.consumer_key
    consumer_secret_twitter = args.consumer_secret
    access_token_twitter = args.access_token
    access_token_secret_twitter = args.access_token_secret

    print(f"Twitter CONSUMER_KEY: {consumer_key_twitter}")
    print(f"Twitter CONSUMER_SECRET: {consumer_secret_twitter}")
    print(f"Twitter ACCESS_TOKEN: {access_token_twitter}")
    print(f"Twitter ACCESS_TOKEN_SECRET: {access_token_secret_twitter}")

    app.run(debug=True, host="0.0.0.0", port=8082, threaded=True)