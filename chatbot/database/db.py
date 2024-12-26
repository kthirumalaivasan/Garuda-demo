from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Retrieve MongoDB URI and database/collection names from environment variables
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION1 = os.getenv("COLLECTION1")
COLLECTION2 = os.getenv("COLLECTION2")

# Connect to MongoDB using the URI
client = MongoClient(MONGO_URI)

# Select the database
db = client[DATABASE_NAME]

# Select collections
collection1 = db[COLLECTION1]
collection2 = db[COLLECTION2]

# Test the connection
print(f"Connected to database: {DATABASE_NAME}")
print(f"Collection1: {COLLECTION1}, Collection2: {COLLECTION2}")