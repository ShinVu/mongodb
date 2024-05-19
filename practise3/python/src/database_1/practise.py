from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,OperationFailure

# Connection URI
MONGO_URI = "mongodb://root:root@mongodb:27017/admin"

# Create a MongoDB client
client = MongoClient(MONGO_URI)

try:
    #Connect to database
    my_database = client['training']
    
    #Connect to collection
    language = my_database['languages']
    
    #Insert to collection
    documents = [
    {"name":"java","type":"object oriented"},
    {"name":"python","type":"general purpose"},
    {"name":"scala","type":"functional"},
    {"name":"c","type":"procedural"},
    {"name":"c++","type":"object oriented"}
    ]
    
    language.insert_many(documents)
    
    #Insert 
    document = {"name": "Haskell", "type": "functional"}
    language.insert_one(document)
    
    #Query
    filter = {"type": "functional"}
    result = language.find(filter)
    for document in iter(result):
        print(document)
    
    #Update 
    filter= {"name": "c++"}
    setUpdate = {"creator": "Bjarne Stroustrup"}
    result = language.update_many(filter,{"$set": setUpdate})
    print(result)
    
    #Delete
    filter= {"type": "functional"}
    result = language.delete_many(filter)
    print(result)
    
    
except ConnectionFailure as ce:
    print("Could not connect to MongoDB:", ce)
    
except OperationFailure as of:
    print("Operation fail", of)

except Exception as e:
    print("Unknown error:", e)
    
finally:
    # Close the connection
    client.close()