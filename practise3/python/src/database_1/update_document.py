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
    
    #Update, add new fields to all document
    result = language.update_many({},{"$set" :{"description" : "programming language"}})
    print(result)
    
    print("\n")
    
    #Update, add creator for all document with value of field name as python
    result = language.update_many({"name": "python"}, {"$set": {"creator": "somebody"}})
    print(result)
    
    print("\n")
    
    #Update, add compile with value true to all document with value of field type as object oriented
    result = language.update_many({"type": "object oriented"}, {"$set": {"compile": True}} )
    print(result)
    
    print("\n")
    
    #Update, increment version by 3 for all document with value of field 'name' as 'python'
    result = language.update_many({"name": "python"}, {"$inc": {"versions": 3}})
    print(result)
    
    
except ConnectionFailure as ce:
    print("Could not connect to MongoDB:", ce)
    
except OperationFailure as of:
    print("Operation fail", of)
    
finally:
    # Close the connection
    client.close()