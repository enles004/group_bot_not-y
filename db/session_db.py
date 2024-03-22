from pymongo import MongoClient
import config

client = MongoClient(config.mongo_url)
db = client.schedule
user = db.users
schedule = db.bot_schedule

