import pymongo, certifi


ca = certifi.where()
connectionString = "mongodb+srv://user_api:hqxPF3wtSl9XQMby@simulatepix.pokky.mongodb.net/SimulaPix?retryWrites=true&w=majority"
mongodbClient = pymongo.MongoClient(connectionString, tlsCAFile=ca, serverSelectionTimeoutMS=5000)
database = mongodbClient['PIX']
dbAccount = database['Account']
# print(dbAccount)
