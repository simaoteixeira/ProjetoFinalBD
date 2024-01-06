# mongo_init.py
import environ
from pymongo import MongoClient

env = environ.Env()
environ.Env.read_env('./ProjetoFinal/.env')

# SET CONSTANTS
DB_NAME = env('DB_NAME')
DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')
DB_MONGO_CONNECTION = env("MONGO_DB_CONNECTION")

print(DB_MONGO_CONNECTION)


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

print(client)

# Use 'bd2' database
db = client[DB_NAME]

print(db)


# Create a collection named 'your_collection_name'
collection = db['product_props']

print(collection)

# Insert a document into the collection (optional)
collection.insert_one({'example_key': 'example_value'})

# Clear al data from collection
collection.delete_many({})

# Close the connection
client.close()
