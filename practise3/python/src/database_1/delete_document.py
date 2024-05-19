from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,OperationFailure

# Connection URI
MONGO_URI = "mongodb://root:root@mongodb:27017/admin"

# Create a MongoDB client
client = MongoClient(MONGO_URI)

try:
    #Connect to database
    my_database = client['my_database']
    
    #Connect to collection
    language = my_database['languages']
    
    #Delete all documents with field 'name'='scalar'
    result = language.delete_many({"name": "scala"})
    print(result)
    
    #Delete all documents with field 'type'='object oriented'
    result = language.delete_many({"type": "object oriented"})
    print(result)
    
    #Delete all documents from collections
    result = language.delete_many({})
    print(result)
    
    
except ConnectionFailure as ce:
    print("Could not connect to MongoDB:", ce)
    
except OperationFailure as of:
    print("Operation fail", of)
    
finally:
    # Close the connection
    client.close()