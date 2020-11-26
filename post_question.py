from datetime import datetime
import time
import random
import pymongo
from pymongo import MongoClient

port = 27017
client = pymongo.MongoClient('localhost', port) 
db = client["291db"]
def generateID(collection):
    random_id = str('q' + ("{:0>3d}".format(random.randint(0,9999999))))
    unique_id = False
    while not unique_id:
        result = collection.find_one({"Id": random_id })
        if result == None:
            unique_id = True
            return random_id
def post_question(uid, db):
    title = input("Please enter a title for the post: ")
    body = input("Please enter a body for the posts: ")
    tags = input("Please enter tags(optional,press enter if no tags), seperate by space: ")
    ID = generateID(db.Posts)
    print(ID)
    now = datetime.now()
    post_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    rst = ''
    #if tags provided
    if (len(tags) > 0):
        Tag = tags.split(" ")
        for item in Tag:
            rst += "<"+str(item)+">"
            #and with userID provided
        if (len(str(uid)) > 0):
            post = {
                "Id": ID,
                "PostTypeId": "1",
                "CreationDate": post_date,
                "Title": title,
                "Tags":rst,
                "Body": "<p>"+body+"</p>",
                "Score": 0,
                "OwnerUserId":uid,
                "ViewCount": 0,
                "AnswerCount": 0,
                "CommentCount": 0,
                "FavoriteCount": 0,
                "ContentLicense": "CC BY-SA 2.5"}               
            db.Posts.insert_one(post)       
        else:
            #tags provided but userID doesn't provided
            post = {
                "Id": ID,
                "PostTypeId": "1",
                "CreationDate": post_date,
                "Title": title,
                "Tags":rst,
                "Body": "<p>"+body+"</p>",
                "Score": 0,
                "ViewCount": 0,
                "AnswerCount": 0,
                "CommentCount": 0,
                "FavoriteCount": 0,
                "ContentLicense": "CC BY-SA 2.5"}               
            db.Posts.insert_one(post)        
            #insert tag into tags collection
        for tag in Tag:
            result = {"TagName": tag}
            if db.Tags.find_one(result) != None:
                db.Tags.update_one({"TagName":tag},{ "$inc": { "Count": 1 } })
            else:
                tagID = generateID(db.Tags)
                newTag = {"Id": tagID,"TagName": tag,"Count": 1}
                db.Tags.insert_one(newTag)

    else:
        #if tags do not provide,but userID provided
        if (len(str(uid)) > 0):
            post = {
                "Id": ID,
                "PostTypeId": "1",
                "CreationDate": post_date,
                "Title": title,
                "OwnerUserId":uid,
                "Body": "<p>"+body+"</p>",
                "Score": 0,
                "ViewCount": 0,
                "AnswerCount": 0,
                "CommentCount": 0,
                "FavoriteCount": 0,
                "ContentLicense": "CC BY-SA 2.5"}            
            db.Posts.insert_one(post) 
        else:
            #if both userID and tags do not provide
            post = {
                "Id": ID,
                "PostTypeId": "1",
                "CreationDate": post_date,
                "Title": title,
                "Body": "<p>"+body+"</p>",
                "Score": 0,
                "ViewCount": 0,
                "AnswerCount": 0,
                "CommentCount": 0,
                "FavoriteCount": 0,
                "ContentLicense": "CC BY-SA 2.5"}              
            db.Posts.insert_one(post) 
    print("Post " +ID+ " saved.")
