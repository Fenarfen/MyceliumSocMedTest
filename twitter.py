# source: https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Manage-Tweets/create_tweet.py

from requests_oauthlib import OAuth1Session
import os
import json

# set keys using below code in another python file or do it manually DOES NOT WORK, SEE BELOW
# ---------------------------------------------------------------------------------------------
# import os
# os.environ['CONSUMER_KEY'] = ask me for test key
# os.environ['CONSUMER_SECRET'] = ask me for test key

# print(os.environ['CONSUMER_KEY']) this prints key to terminal, so you know it's correct
# print(os.environ['CONSUMER_SECRET']) this prints key to terminal, so you know it's correct
# ---------------------------------------------------------------------------------------------

# above doesn't work, need to research a more viable option to protect the keys during collaboration on github
# for now I'll just remove the key for github

consumer_key = '' # ASK FOR KEYS, NOT GONNA PUT THEM ON GITHUB
consumer_secret = '' # ASK FOR KEYS, NOT GONNA PUT THEM ON GITHUB

# Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls,
# quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
payload = {"text": "Hello world!"}

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Making the request
response = oauth.post(
    "https://api.twitter.com/2/tweets",
    json=payload,
)

if response.status_code != 201:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print("Response code: {}".format(response.status_code))

# Saving the response as JSON
json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))
