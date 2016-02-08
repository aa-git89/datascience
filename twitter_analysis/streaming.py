from slistener import SListener
import time, tweepy, sys

## auth. 
## TK: Edit the username and password fields to authenticate from Twitter.
#username = ''
#password = ''
#auth     = tweepy.auth.BasicAuthHandler(username, password)
#api      = tweepy.API(auth)

## Eventually you'll need to use OAuth. Here's the code for it here.
## You can learn more about OAuth here: https://dev.twitter.com/docs/auth/oauth
consumer_key        = "your credentials"
consumer_secret     = "your credentials"
access_token        = "your credentials"
access_token_secret = "your credentials"

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api  = tweepy.API(auth)

def main( mode = 1 ):
	# Enter the text you will like to track below
    track  = ['#SuperBowl']
    follow = []
            
    listen = SListener(api, 'SuperBowlHashtag')
    stream = tweepy.Stream(auth, listen)

    print "Streaming started on %s users and %s keywords..." % (len(track), len(follow))

    try: 
        stream.filter(track = track, follow = follow)
        #stream.sample()
    except:
        print "error!"
        stream.disconnect()

if __name__ == '__main__':
    main()