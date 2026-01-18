from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("mongo_connection_string")

client = AsyncIOMotorClient(MONGO_URL)
db = client["expenseManagement"]

transactions_collection = db["transactions"]
uploads_collection = db["uploads"]
categories_collection = db["categories"]
users_collection = db["users"]
