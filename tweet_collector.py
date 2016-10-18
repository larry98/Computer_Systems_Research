
# Lawrence Wang

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import keys
import json
import time
import datetime
import sys
import os

key_words = ['hillary', 'clinton', 'donald', 'trump', 'kaine', 'pence', 
			 'liberal', 'conservative', 'election2016', 'democrat', 
			 'republican', 'gop', 'imwithher', 'crookedhillary', 'maga', 
			 'lockherup']


def parse_user(author):
	user = {}
	user['id'] = author['id_str']
	user['location'] = author['location']
	user['geo_enabled'] = author['geo_enabled']
	user['handle'] = author['screen_name']
	user['name'] = author['name']
	return user


def parse_tweet(status):
	tweet = {}
	tweet['author'] = parse_user(status['user'])
	if tweet['author']['location'] == None:
		return None
	tweet['text'] = status['text']
	tweet['id'] = status['id_str']
	tweet['retweeted'] = status['retweeted']
	tweet['retweet_count'] = status['retweet_count']
	tweet['favorite_count'] = status['favorite_count']
	tweet['date'] = status['created_at']
	tweet['coordinates'] = status['coordinates']
	tweet['hashtags'] = [ht['text'] for ht in status['entities']['hashtags']]
	return json.dumps(tweet)


class MyListener(StreamListener): 

	def __init__(self, num):
		super(MyListener, self).__init__()
		self.fout = open('tweets%d.json' %num, 'a')
		self.counter = 0
		self.buffer_size = 1000

	def on_connect(self):
		print("Connected")

	def on_status(self, status): 
		try: 
			tweet = parse_tweet(status._json)
			if tweet == None:
				return True
			self.fout.write(tweet)
			self.counter += 1
			if self.counter >= self.buffer_size:
				self.fout.flush()
				os.fsync(self.fout.fileno())
				self.counter = 0
			return True
		except BaseException as e:
			print("Error on status: %s" %str(e))
			time.sleep(5)
			return True

	def on_error(self, status):
		print("Error #: %s" %str(status))
		return False


if __name__ == "__main__":

	i = int(sys.argv[1]) - 1
	key = keys.key_list[i]
	auth = OAuthHandler(key['API_KEY'], key['API_SECRET'])
	auth.set_access_token(key['ACCESS_TOKEN'], key['ACCESS_TOKEN_SECRET'])

	while True:
		try:
			twitterStream = Stream(auth, MyListener(num=i+1))
			twitterStream.filter(track=key_words, languages=['en'])
		except BaseException as e:
			print("Error: %s" %str(e))
			time.sleep(60)
