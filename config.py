import os

from dotenv import load_dotenv

load_dotenv()
token_tele = os.getenv("TOKEN_TELE")
message_id = os.getenv("MESSAGE_ID")
mongo_url = os.getenv("MONGO_URL")