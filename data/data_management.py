from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from .variables import MONGODB_CLUSTER_NAME, MONGODB_PASSWORD, MONGODB_USERNAME, MONGODB_COLLECTION_NAME, MONGODB_DATABASE_NAME
from logging_config import configure_logger

logger = configure_logger(__name__)


def get_database():
 
   CONNECTION_STRING = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER_NAME}.ahiefpd.mongodb.net/?retryWrites=true&w=majority"

   client = MongoClient(CONNECTION_STRING)
 
   return client[MONGODB_DATABASE_NAME]


def insert_data(mongo_db, data):

   db_collection = mongo_db[MONGODB_COLLECTION_NAME]

   try:
      db_collection.insert_many(data)
      return True  
   
   except BulkWriteError as e:
      logger.error(f"Error inserting data: \n{e}")
      return False 


def get_existing_ids(mongo_db):
    
    db_collection = mongo_db[MONGODB_COLLECTION_NAME]

    if MONGODB_COLLECTION_NAME in mongo_db.list_collection_names():
        existing_ids = db_collection.distinct("ad_id")
        return existing_ids
    
    else:
        return []


def query_all_data(mongo_db):
    db_collection = mongo_db[MONGODB_COLLECTION_NAME]

    if MONGODB_COLLECTION_NAME in mongo_db.list_collection_names():
        all_data = list(db_collection.find())
        return all_data
    
    else:
        return []


def delete_all_data(mongo_db):
    db_collection = mongo_db[MONGODB_COLLECTION_NAME]

    if MONGODB_COLLECTION_NAME in mongo_db.list_collection_names():
        db_collection.delete_many({})
        return True
    
    else:
        return False



if __name__ == "__main__":   
    pass