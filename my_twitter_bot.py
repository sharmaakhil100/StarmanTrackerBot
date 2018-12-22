import tweepy
import time
import urllib.request
from bs4 import BeautifulSoup # for parsing HTML

print('this is my twitter bot')

CONSUMER_KEY = 'kimv5ExkuGmwJNn1fQfL7OMo0'
CONSUMER_SECRET = 'FIuPKWLb0CeU9JHuNyVi3RYrmLPsqr9q8yi9NFEpVobEA2g5BU'
ACCESS_KEY = '732728506510008320-jHjf5KVsI5CgVROgQPb2CTgk04V0ZAG'
ACCESS_SECRET = 'nIMTytpFgrSK7VmgTWGOgl4NikeHdmP4m2YVbPwox3POF'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

#DEV NOTE: use 1075836624099893248 for testing

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

class AppURLopener(urllib.request.FancyURLopener):
    # We can get blocked (error 403 Forbidden) because of our use of urllib based on the user agent. We use this class to override the user-agent with Mozilla.
    version = "Mozilla/5.0"

def where_is_roadster():
    """
    Returns string containing information about Roadster's position in outer space in relation to the Earth and Mars
    """
    opener = AppURLopener()
    response = opener.open('https://where-is-tesla-roadster.space/live')
    html = BeautifulSoup(response.read(),"html.parser")
    for link in html.find_all('meta'):
        if type(link.get('content')) == str and "current distance" in link.get('content'):
            return link.get('content')

# Get the message containing the information on the Roadster's distance from Earth and Mars
distance = where_is_roadster()

def reply_to_tweets():
    print('retrieving and replying to tweets...')
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#wheresroadster' in mention.full_text.lower() or 'roadster' in mention.full_text.lower():
            print('found roadster!')
            print('responding back...')
            api.update_status('@' + mention.user.screen_name + " " + 
                    distance[distance.find("Roadster's"):], mention.id)

while True:
    reply_to_tweets() # call the function which does all the replying
    time.sleep(900) # loop code every 15 MINUTES

"""
References/Resources Used:
    1) https://www.youtube.com/watch?v=EiIw8umi-MM
    2) https://stackoverflow.com/a/31758803
    3) https://docs.python.org/3/library/urllib.request.html
    4) https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""
