import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')

client = pymongo.MongoClient(DATABASE_URI)
db = client['skatersAPI']
skaters_collection = db['skaters']

def add_skater_database(data):
    try:
        skaters_collection.insert_one(data)
        print(f'succesfully added {data['fName']} {data['lName']}')
        return True
    except Exception as e:
        print(f'ERROR: {e}')

def search_for_skater(skater):
    data = list(skaters_collection.find(skater, {'_id': False}))
    return data