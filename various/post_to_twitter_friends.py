#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import twitter


# @deefuzz_test3
key='146002442-qgtArE6YrpLfL6h51LnE5TA9skcKhOqDraNDaOY'
secret='8RWoZjllOv52PUmXbLJcu5qunY8qAa6V6pyLGBHEcg'

# @parisson_studio
#key='223431436-8uYqGM0tLHBiMbk6Bt39oBfwXpylfLcr7t6bs311'
#secret='SzWD3fDgBpw9qwNNrYarXTcRJSTklp0PpKXg7Iw'

# Twitter DeeFuzzer keys
DEEFUZZER_CONSUMER_KEY = 'ozs9cPS2ci6eYQzzMSTb4g'
DEEFUZZER_CONSUMER_SECRET = '1kNEffHgGSXO2gMNTr8HRum5s2ofx3VQnJyfd0es'


class Twitter:

    def __init__(self, access_token_key, access_token_secret):
        import twitter
        self.consumer_key = DEEFUZZER_CONSUMER_KEY
        self.consumer_secret = DEEFUZZER_CONSUMER_SECRET
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        self.api = twitter.Api(consumer_key=self.consumer_key,
                               consumer_secret=self.consumer_secret,
                               access_token_key=self.access_token_key,
                               access_token_secret=self.access_token_secret)
        self.followers = self.api.GetFollowers()
        self.friends = self.api.GetFriends()
        
    def post(self, message):
        try:
            self.api.PostUpdate(message)
        except:
            pass

    def print_followers(self):
        print str(len(self.followers)) + ' Followers:'
        for f in self.followers:
            print ' ' + f.screen_name
    
    def send_private_mess(self, mess, tags):
        for f in self.followers:
            self.api.PostDirectMessage(f.screen_name, mess + ' #' + (' #').join(tags))

    def print_friends(self):
        print str(len(self.friends)) + ' Friends:'
        for f in self.friends:
            print ' ' + f.screen_name
    
    def send_friends_mess(self, mess, tags):
        for f in self.followers:
            self.post('@' + f.screen_name + ' ' + mess  + ' #' + ' #'.join(tags))
    
    
if __name__ == '__main__':
    mess = 'Hello World ! TEST ! RVSP' 
    tags = ['t35t', 'test', 'TesT']
    
    twitt = Twitter(key, secret)
    
    twitt.print_followers()
    twitt.print_friends()
    
    twitt.send_private_mess(mess, tags)
    twitt.send_friends_mess(mess, tags)
    
    