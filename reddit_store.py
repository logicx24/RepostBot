from pymongo import MongoClient

class RedditStore(object):

	def __init__(self, db_name, collection_name, id_prop, date_prop):
		self.mongo_client = self.get_client()
		self.db_name = db_name
		self.collection_name = collection_name

		self.id_property = id_prop
		self.date_property = date_prop

	def get_client(self):
		return MongoClient()

	def get_collection(self):
		return self.mongo_client[self.db_name][self.collection_name]

	def save_submission(self, submission_dict):
		self.get_collection().update_one(
			{self.id_property: submission_dict[self.id_property]},
			submission_dict,
			True
		)
	
	def get_submissions_after_date(date):
		self.get_collection().find(
			filter={self.date_property: {"$gte": date}}
		)
