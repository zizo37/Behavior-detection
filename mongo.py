from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def connect_to_mongo():
    try:
        # Retrieve MongoDB URI and database name from environment variables
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME")
        collection_name = os.getenv("COLLECTION_NAME")
        
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        print("Connected to MongoDB successfully!")
        
        # Access the database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        return client, collection
    except Exception as e:
        print("Failed to connect to MongoDB:", e)
        return None, None

def fetch_comments(collection):
    try:
        # Retrieve all comments (example: assuming field "comment" exists)
        comments = list(collection.find({}, {"_id": 0, "comment": 1}))
        comments_text = [comment["comment"] for comment in comments]
        return comments_text
    except Exception as e:
        print("Error fetching comments:", e)
        return []

if __name__ == "__main__":
    # Connect to the collection
    client, collection = connect_to_mongo()
    if collection:
        try:
            # Fetch and print comments
            comments = fetch_comments(collection)
            print(f"Retrieved {len(comments)} comments:")
            for i, comment in enumerate(comments, 1):
                print(f"{i}. {comment}")
        finally:
            client.close()
