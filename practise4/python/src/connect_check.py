from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

try:
    #Get connection URI
    MONGO_URI = os.environ['MONGODB_URI']
except KeyError as e:
    print(f"Environment variable {e} not found. Please set it.")

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
