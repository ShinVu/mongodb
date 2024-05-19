from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo import ASCENDING, DESCENDING
# Connection URI
MONGO_URI = "mongodb://root:root@mongodb:27017/admin"

# Create a MongoDB client
client = MongoClient(MONGO_URI)

try:
    # Connect to database and collection
    my_database = client['my_database']
    big_data_2 = my_database['big_data_2']
    
    # Insert sample data
    marks_data = [
    {"name": "Ramesh", "subject": "maths", "marks": 87},
    {"name": "Ramesh", "subject": "english", "marks": 59},
    {"name": "Ramesh", "subject": "science", "marks": 77},
    {"name": "Rav", "subject": "maths", "marks": 62},
    {"name": "Rav", "subject": "english", "marks": 83},
    {"name": "Rav", "subject": "science", "marks": 71},
    {"name": "Alison", "subject": "maths", "marks": 84},
    {"name": "Alison", "subject": "english", "marks": 82},
    {"name": "Alison", "subject": "science", "marks": 86},  
    {"name": "Steve", "subject": "maths", "marks": 81},
    {"name": "Steve", "subject": "english", "marks": 89},
    {"name": "Steve", "subject": "science", "marks": 77},
    {"name": "Jan", "subject": "english", "marks": 0, "reason": "absent"}
    ]   
    
    big_data_2.insert_many(marks_data)
    
    # Limit
    result = big_data_2.aggregate([{"$limit": 2}])
    for document in iter(result):
        print(document)

    print("\n")
    
    # Sorting (ascending)
    result = big_data_2.aggregate([{"$sort": {"marks": ASCENDING}}])
    for document in iter(result):
        print(document)
    
    print("\n")
     
    # Sorting (descending)
    result = big_data_2.aggregate([{"$sort": {"marks": DESCENDING}}])
    for document in iter(result):
            print(document)        
    
    print("\n")
    
    # Group by 
    result = big_data_2.aggregate([
        {"$group": 
            {
                "_id": "$subject",
                "average": 
                    {
                        "$avg": "$marks"
                    }
            }
        }
        ])
    for document in iter(result):
        print(document)
               
    print("\n")
    
    #Sum of marks, group by objects
    result = big_data_2.aggregate(
        [
            {
                "$group":
                    {
                        "_id": "$subject",
                        "sum": {"$sum": "$marks"}
                    }
            }
        ]
    )
    
    for document in iter(result):
        print(document)
               
    print("\n")
    
    #Max of marks, group by objects
    result = big_data_2.aggregate(
        [
            {
                "$group":
                    {
                        "_id": "$subject",
                        "max": {"$max": "$marks"}
                    }
            }
        ]
    )
    
    for document in iter(result):
        print(document)
               
    print("\n")
    
    #Min of marks, group by each student
    result = big_data_2.aggregate(
        [
            {
                "$group":
                    {
                        "_id": "$name",
                        "min": {"$min": "$marks"}
                    }
            }
        ]
    )
    
    for document in iter(result):
        print(document)
               
    print("\n")
    
    #Top two subjects, based on average marks
    result = big_data_2.aggregate(
        [
            {
                "$group":
                    {
                        "_id": "$subject",
                        "avg": {"$avg": "$marks"}
                    }
            },
            {
                "$sort": 
                    {
                        "avg" : DESCENDING
                    }
            },
            {
                "$limit": 2
            }
        ]
    )
    
    for document in iter(result):
        print(document)
               
    print("\n")
    
except ConnectionFailure as ce:
    print("Could not connect to MongoDB:", ce)
finally:
    # Close the connection
    client.close()
