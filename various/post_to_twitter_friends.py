#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import twitter


# @deefuzz_test3
test_key='146002442-qgtArE6YrpLfL6h51LnE5TA9skcKhOqDraNDaOY'
test_secret='8RWoZjllOv52PUmXbLJcu5qunY8qAa6V6pyLGBHEcg'

# @parisson_studio
ps_key='223431436-8uYqGM0tLHBiMbk6Bt39oBfwXpylfLcr7t6bs311'
ps_secret='SzWD3fDgBpw9qwNNrYarXTcRJSTklp0PpKXg7Iw'

# @parisson_com
pc_key='241046394-MpI5YrkgHSjW0Ab4WIlU0nJruGqesLueCWDJ1qtx'
pc_secret='6gRzqDvqkjhRzFCfetdWfZYPQdbvQQhVEhhGHQ90JCM'

# Twitter DeeFuzzer keys
DEEFUZZER_CONSUMER_KEY = 'ozs9cPS2ci6eYQzzMSTb4g'
DEEFUZZER_CONSUMER_SECRET = '1kNEffHgGSXO2gMNTr8HRum5s2ofx3VQnJyfd0es'

escape = ['parisson_studio', 'parisson_com', 'kvraudio']

class Twitter(object):

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
        self.followers = self.get_followers()
        self.friends = self.get_friends()
        
    def post(self, message):
        try:
            self.api.PostUpdate(message)
        except:
            pass

    def get_friends(self):
        l = []
        for f in self.api.GetFriends():
            l.append(f.screen_name)
        return l
    
    def get_followers(self):
        l = []
        for f in self.api.GetFollowers():
            l.append(f.screen_name)
        return l
    
    def send_private_mess(self, mess, tags):
        for f in self.followers:
            self.api.PostDirectMessage(f, mess + ' #' + (' #').join(tags))

    def send_friends_mess(self, mess, tags):
        mess_header = mess
        for f in self.friends:
            if not f in escape:
                mess = '@' + f + ' ' + mess_header  + ' #' + ' #'.join(tags)
                print mess
                self.post(mess)
            
    def add_friends(self, friends):
        for f in friends:
            if not f in self.friends and not f in escape:
                self.api.CreateFriendship(f)

if __name__ == '__main__':
    mess = 'TC-202 Case : the mobile media solution now released by Parisson http://bit.ly/gSvqaF'
    tags = ['proaudio', 'broadcast']
    
    print ('IN')
    twitt_in = Twitter(ps_key, ps_secret)
    print str(len(twitt_in.followers)) + ' Followers:'
    print twitt_in.followers
    print str(len(twitt_in.friends)) + ' Friends:'
    print twitt_in.friends
    
    print ('OUT')
    twitt_out = Twitter(pc_key, pc_secret)
    print str(len(twitt_out.followers)) + ' Followers:'
    print twitt_out.followers
    print str(len(twitt_out.friends)) + ' Friends:'
    print twitt_out.friends
    
    #twitt_out.add_friends(twitt_in.friends)
    #twitt.send_private_mess(mess, tags)
    twitt_out.send_friends_mess(mess, tags)
    
    print 'OK'
    
    