import os

from dotenv import load_dotenv

load_dotenv()
psql_url = os.getenv("PSQL_URL")
token_tele = os.getenv("TOKEN_TELE")
message_id = os.getenv("MESSAGE_ID")
