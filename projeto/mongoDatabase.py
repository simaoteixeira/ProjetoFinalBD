import pymongo
from environ import environ

env = environ.Env()
environ.Env.read_env()

db = pymongo.MongoClient(env('MONGO_DB_CONNECTION'))[env('DB_NAME')]["product_props"]