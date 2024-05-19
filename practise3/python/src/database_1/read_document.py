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
    
    #Count document
    num_of_documents = language.count_documents({})
    print(num_of_documents)
    
    print("\n")
    
    #Find one document
    document = language.find_one({})
    print(document)
    
    print("\n")
     
    #Find multiple document
    documents = language.find({})
    for document in iter(documents):
        print(document)
    
    print("\n")
     
    #Find and limit to n number of documents
    documents = language.find({}).limit(2)
    for document in iter(documents):
        print(document)
    
    print("\n")
    
    #Query for python language
    documents = language.find({"name": "python"})
    for document in iter(documents):
        print(document)

    print("\n")
    
    #Query for object oriented language
    documents = language.find({"type": "object oriented"})
    for document in iter(documents):
        print(document)
    
    print("\n")
    
    #Query and project only name in the documents
    documents = language.find({},{'name': True})
    for document in iter(documents):
        print(document)
        
    print("\n")
    
    #Query and project all except for name in the documents
    documents = language.find({},{"name": False})
    for document in iter(documents):
        print(document)
        
    print("\n")
    
    #Query with filter by name, and project
    documents = language.find({"name" : "python"},{"name": True})
    for document in iter(documents):
        print(document)
    
    print("\n")
    
except ConnectionFailure as ce:
    print("Could not connect to MongoDB: \n", ce)
    
except OperationFailure as of:
    print("Operation fail: \n", of)
    
finally:
    # Close the connection
    client.close()