from pymongo import MongoClient
import config

client = MongoClient(config.mongo_url)
db = client.schedule_group
schedule = db.schedule

