from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo import ASCENDING, DESCENDING

# Connection URI
MONGO_URI = "mongodb://root:root@mongodb:27017/admin"

# Create a MongoDB client
client = MongoClient(MONGO_URI)

try:
    # Connect to database and collection
    my_database = client['training']
    mongodb_glossary = my_database['mongodb_glossary']
   
    #Insert sample data
    data = [{"database":"a database contains collections"},
    {"collection":"a collection stores the documents"},
    {"document":"a document contains the data in the form of key value pairs."}]
    
    mongodb_glossary.insert_many(data)
    
    #Query all
    result = mongodb_glossary.find({})
    for document in iter(result):
        print(document)
    
    
except ConnectionFailure as ce:
    print("Could not connect to MongoDB:", ce)
finally:
    # Close the connection
    client.close()
