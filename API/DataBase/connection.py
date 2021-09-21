import pymongo

connectionString = "A"
mongodbClient = pymongo.MongoClient(connectionString, serverSelectionTimeoutMS=5000)
database = mongodbClient['SimulatePix']
dbAccount = database['Account']
