from slistener import SListener
import time, tweepy, sys

## auth. 
## TK: Edit the username and password fields to authenticate from Twitter.
#username = 'sharma_amandeep'
#password = ''
#auth     = tweepy.auth.BasicAuthHandler(username, password)
#api      = tweepy.API(auth)

## Eventually you'll need to use OAuth. Here's the code for it here.
## You can learn more about OAuth here: https://dev.twitter.com/docs/auth/oauth
consumer_key        = "lyrn3NiLyyVbeWQpsBNKQgHWt"
consumer_secret     = "zQxhaw3bNcWd1dX8o3feuNo3k3hyFc3BCFDkxUCS4uRXNPcS74"
access_token        = "216090711-wFkgMVSLVccXoI7IlMedjNaq3QwAWnBRbIYnl9L5"
access_token_secret = "gaXQ1kJocSf8xdsW2KKBNHQqVSovnAlfS0DG8vgDI3Aom"

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api  = tweepy.API(auth)

def main( mode = 1 ):
    track  = ['degea', 'de gea','De Gea','de gea','david de gea','David De Gea','D_DeGea']
    follow = []
            
    listen = SListener(api, 'degea')
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