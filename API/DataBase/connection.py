import pymongo

connectionString = "<your_connectionString>"
mongodbClient = pymongo.MongoClient(connectionString, serverSelectionTimeoutMS=5000)
database = mongodbClient['SimulatePix']
dbAccount = database['Account']
