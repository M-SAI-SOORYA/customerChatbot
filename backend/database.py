from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['MONGODB_URL'] = os.getenv("MONGODB_URL")
MONGO_URI=os.getenv("MONGODB_URL")

client = AsyncIOMotorClient(MONGO_URI)
db = client["conversational_ai"]
