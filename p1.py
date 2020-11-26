import pymongo
from pymongo import MongoClient
import json
import time
import sys
def load():
    port = int(sys.argv[1])
    startTime = time.time()    
    client = pymongo.MongoClient('localhost', port)     
    db = client["291db"]
    collist = db.list_collection_names()
    if "Posts" in collist:
        client.drop_database('Posts')
    elif "Tags" in collist:
        client.drop_database('Tags')
    elif "Votes" in collist:
        client.drop_database('Votes')
    Posts = db["Posts"]
    Tags = db["Tags"]
    Votes = db["Votes"]

    #insert posts into Posts
    Posts.delete_many({})
    with open ('Posts.json') as P:
        data1 = json.load(P)["posts"]["row"]
    if isinstance(data1, list):
        Posts.insert_many(data1)
    else:
        Posts.insert_one(data1)    
    #insert tags into Tags   
    Tags.delete_many({})
    with open ('Tags.json') as T:
        data2 = json.load(T)["tags"]["row"]
    if isinstance(data2, list):
        Tags.insert_many(data2)
    else:
        Tags.insert_one(data2)    
    #insert votes into Votes   
    Votes.delete_many({})
    with open ('Votes.json') as V:
        data3 = json.load(V)["votes"]["row"]
    if isinstance(data3, list):
        Votes.insert_many(data3)
    else:
        Votes.insert_one(data3)    
    timeTaken = time.time() - startTime
    print("Sucessfully load, taken " + str(timeTaken) + " seconds ")    
def main():
    load()
main()