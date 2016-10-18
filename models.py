
# Lawrence Wang

from peewee import *

db = SqliteDatabase(DATABASE)


class BaseModel(Model):
	class Meta:
		database = db


class Tweet(BaseModel):
	id = IntegerField(primary_key=True)
	text = TextField()
	user_id = ForeignKeyField(User)
	date = DateField()
	retweeted = BooleanField()
	retweet_count = IntegerField()
	favorite_count = IntegerField()
	hashtags = TextField()


class User(BaseModel):
	id = IntegerField(primary_key=True)
	handle = CharField()
	name = CharField()
	location = CharField()
	county_id = ForeignKeyField(County)


class County(BaseModel):
	pass