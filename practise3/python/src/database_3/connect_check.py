from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Connection URI
MONGO_URI = "mongodb://root:root@mongodb:27017/admin"

# Create a MongoDB client
client = MongoClient(MONGO_URI)

try:
    # Connect to the server and get server info
    server_info = client.server_info()
    print("Connected to MongoDB server version:", server_info["version"])

except ConnectionFailure as ce:
    print("Could not connect to MongoDB:", ce)
finally:
    # Close the connection
    client.close()
