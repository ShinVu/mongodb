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
    
    #Insert sample data
    # documents = [{ "account_no": i+1, "balance": round(random.random() * 20000) } for i in range(200000)]
    
    # result = bigdata.insert_many(documents)
    # print(result)
    
    #Query and see the execution plan (before using index)
    result = bigdata.find({"account_no": 58982}).explain()
    with open("explain_result.json","w+") as file:
        json.dump(result,file,indent=4)
    
    #Add index
    result = bigdata.create_index([("account_no", ASCENDING)])
    print(result)
    
    #check if index exists
    result = bigdata.index_information()
    print(result)
    
    #Query and see the execution plan (after using index)
    result = bigdata.find({"account_no": 58982}).explain()
    with open("explain_result_index.json","w+") as file:
        json.dump(result,file,indent=4)

    #Drop index 
    bigdata.drop_index("account_no_1")
    
    #check if index exists
    result = bigdata.index_information()
    print(result)

except ConnectionFailure as ce:
    print("Could not connect to MongoDB:", ce)
finally:
    # Close the connection
    client.close()
