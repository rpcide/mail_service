from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

dbClient = MongoClient(os.getenv("MONGO_URL")).dev
print(os.getenv("MONGO_URL"))