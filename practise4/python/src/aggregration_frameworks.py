from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
import os
import json

try:
    #Get connection URI
    MONGO_URI = os.environ['MONGODB_URI']
except KeyError as e:
    print(f"Environment variable {e} not found. Please set it.")

# Create a MongoDB client
client = MongoClient(MONGO_URI)

try:
    #Aggregration
    database = client.get_database("sample_mflix")
    
    movies_collection = database.get_collection("movies")
    
    #Count all documents
    # results = movies_collection.aggregate(
    #     [
    #         {"$count": "count"}
    #     ]
    # )
    
    # for document in iter(results):
    #     print(document)
        
    #Sorts and limits
    results = movies_collection.aggregate(
        [
            {
                "$sort": 
                    {
                        "num_mflix_comments": DESCENDING,
                        "runtime": ASCENDING
                    }
            },
            {
                "$limit": 5
            },
        ]
    )

    with open("result_1.json", "w+") as file:
        json.dump(list(results),file,default=str,indent=4)
        
    #Match,Project
    results = movies_collection.aggregate(
        [
            {
                "$match":
                    {
                        "genres": {"$eq": "Comedy"}
                    }
            },
            {
                "$project":
                    {
                        "runtime": 1,
                        "title": 1
                    }
            },
            {
                "$sort":
                    {
                        "runtime": DESCENDING
                    }
            },
            {
                "$limit": 10
            }
        ]
    )
    
    with open("result_2.json", "w+") as file:
        json.dump(list(results),file,default=str,indent=4)
    
    #Match with array field - Find all movies with genres Comedy and Romance
    results = movies_collection.aggregate(
        [
            {
                "$match":
                    {
                        "genres": {"$all": ["Comedy", "Romance"]}
                    }
            },
        
            {
                "$limit": 10
            }
        ]
    )
    
     #Match with object field
    results = movies_collection.aggregate(
        [
            {
                "$match":
                    {
                        "imdb.rating": {"$gte": 7.0, "$lte": 10}
                    }
            },
        
            {
                "$limit": 10
            }
        ]
    )
    with open("result_4.json", "w+") as file:
        json.dump(list(results),file,default=str,indent=4)
        
    #Bucket - Group by runtime and get set of genres for that runtime
    results = movies_collection.aggregate(
        [
            {
                "$unwind": "$genres"
           },
           {
               "$bucket": 
                   {
                        "groupBy": "$runtime",
                        "boundaries": [0,5,10],
                        "default": "Others",
                        "output": {
                            "genres": {"$addToSet": "$genres"}
                        }
                    }
           },
            {
               "$project": 
                   {
                       "_id": 1,
                       "genres": 1
                   }
            },
        ]
    )
    
    with open("result_5.json", "w+") as file:
        json.dump(list(results),file,default=str,indent=4)
        
    #Faucet 
    results = movies_collection.aggregate(
        [
            {
                "$facet":
                    {
                     "CountByGenres": 
                         [
                             {
                                 "$unwind":
                                     {
                                        "path": "$genres",
                                        "preserveNullAndEmptyArrays": True
                                     }
                             },
                             {
                                 "$sortByCount":"$genres"
                             }
                         ],
                        "CategoriedByRuntime":
                            [
                                {
                                    "$match": 
                                        {
                                            "runtime": 
                                                {
                                                    "$exists": True
                                                }
                                        }
                                },
                                {
                                      "$bucket": 
                                        {
                                            "groupBy": "$runtime",
                                            "boundaries": [  0, 5,10,15],
                                            "default": "Other",
                                            "output": 
                                                {
                                                "count": { "$sum": 1 },
                                                "titles": { "$push": "$title" }
                                                }
                                        }
                                }
                            ],
                        "CategorizedByYear": [
                            {
                                "$match":
                                    {
                                        "year": {"$exists": True}
                                    }
                            },
                            {
                                "$bucketAuto": 
                                    {
                                        "groupBy": "$year",
                                        "buckets": 4,
                                    }
                            }
                        ]
                    }
            }
        ]
    )
    with open("result_6.json", "w+") as file:
        json.dump(list(results),file,default=str,indent=4)
    
    #Group by
    results = movies_collection.aggregate(
        [
            {
                "$group":
                    {
                        "_id": "$metacritic",
                        "avg_imdb_rating": {"$avg": "$imdb.rating"},
                        "avg_tomatoes_viewer_rating": {"$avg": "$tomotoes.viewer.rating"},
                        "avg_tomatoes_critic_rating": {"$avg": "$tomotoes.critic.rating"}
                    }
            }
        ]
    )
    with open("result_7.json", "w+") as file:
        json.dump(list(results),file,default=str,indent=4)
        
    #Atlas search - Get all movies that must have classic, must not have horror and should have comedy plot
    results = movies_collection.aggregate(
        [
            {
            "$search":
                {
                    "compound":
                        {
                            "must": [{
                                "text": {
                                    "query": "classic",
                                    "path": "fullplot"
                                }
                            }],
                            "mustNot": [{
                                "text": {
                                    "query": "horror",
                                    "path": "fullplot"
                                }
                            }],
                            "should":[{
                                "text": {
                                    "query": "comedy",
                                    "path": "fullplot"
                                }
                            }]
                        },
                }
            }
        ]
    )
    with open("result_8.json", "w+") as file:
        json.dump(list(results),file,default=str,indent=4)

except ConnectionFailure as ce:
    print("Could not connect to MongoDB:", ce)
finally:
    # Close the connection
    client.close()
