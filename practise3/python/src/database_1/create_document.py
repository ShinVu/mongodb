from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,OperationFailure

# Connection URI
MONGO_URI = "mongodb://root:root@mongodb:27017/admin"

# Create a MongoDB client
client = MongoClient(MONGO_URI)

try:
    # Create a new database
    my_database = client["my_database"]

    # Create a new collection within the database
    my_collection = my_database["languages"]
    
    # Insert a collection
    documents = [{"name":"java","type":"object oriented"},{"name":"python","type":"general purpose","versions":201}]
    my_collection.insert_many(documents)
    
except ConnectionFailure as ce:
    print("Could not connect to MongoDB:", ce)
    
except OperationFailure as of:
    print("Operation fail", of)
    
finally:
    # Close the connection
    client.close()