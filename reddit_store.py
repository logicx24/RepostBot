from pymongo import MongoClient
from datetime import datetime

class RedditStore(object):

	def __init__(self, db_name, collection_name, id_prop, date_prop, posted_prop):
		self.mongo_client = self.get_client()
		self.db_name = db_name
		self.collection_name = collection_name

		self.id_property = id_prop
		self.date_property = date_prop
		self.posted_property = posted_prop

	def get_client(self):
		return MongoClient()

	def get_collection(self):
		return self.mongo_client[self.db_name][self.collection_name]

	def save_submission(self, submission_dict):
		submission_dict["inserted_at"] = datetime.now()
		self.get_collection().replace_one(
			{self.id_property: submission_dict[self.id_property]},
			submission_dict,
			upsert=True
		)
	
	def get_unposted_submissions_after_date(self, date):
		return self.get_collection().find(
			filter={self.date_property: {"$gte": date}, self.posted_property: False}
		)

	def get_submissions_after_date(self, date):
		return self.get_collection().find(
			filter={self.date_property: {"$gte": date}}
		)

	def get_subreddit_submissions_after_date(self, date, subreddit):
		return self.get_collection().find(
			filter={self.date_property: {"$gte": date}, "subreddit": subreddit}
		)

	def mark_posted(self, submission_dict):
		submission_dict[self.posted_property] = True
