from pymongo import MongoClient
from pymongo import ASCENDING,DESCENDING
from pymongo.errors import ConnectionFailure
import math
import random
import json

# Connection URI
MONGO_URI = "mongodb://root:root@mongodb:27017/admin"

# Create a MongoDB client
client = MongoClient(MONGO_URI)

try:
    database = client['my_database']
    
    bigdata = database['bigdata']
    
    #Create index on 'balance' field
    bigdata.create_index([("balance",ASCENDING)], name="balance_index")
    
    #Check if index exists
    index_information = bigdata.index_information()
    print(index_information)

    #Query
    explain_query = bigdata.find({"balance": 10000}).explain()
    with open("explain_result_index_2.json","w+") as file:
        json.dump(explain_query,file,indent=4)
    
    #Drop index
    bigdata.drop_index("balance_index")
    
    #Query
    explain_query = bigdata.find({"balance": 10000}).explain()
    with open("explain_result_2.json", "w+") as file:
        json.dump(explain_query,file,indent=4)
        
        
except ConnectionFailure as ce:
    print("Could not connect to MongoDB:", ce)
finally:
    # Close the connection
    client.close()
