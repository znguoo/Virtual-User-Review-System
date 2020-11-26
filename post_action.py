from datetime import datetime
import time
import random
import pymongo
from pymongo import MongoClient

def generateID(collection):
    #generate unique id
    random_id = str("{:0>3d}".format(random.randint(0,9999999)))
    unique_id = False
    while not unique_id:
        result = collection.find_one({"Id": random_id })
        if result == None:
            unique_id = True
            return random_id

def answer_question(qid, uid, db):
    title = input("Please enter a title for the post: ")
    body = input("Please enter a body for the posts: ")
    ID = 'a'+ generateID(db.Posts)
    now = datetime.now()
    post_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    #for uid provided
    if (len(str(uid)) > 0):
        post = {
            "Id": ID,
            "PostTypeId": "2",
            "CreationDate": post_date,
            "Body": "<p>"+body+"</p>",
            "ParentId": qid,
            "OwnerUserId":uid,
            "Score": 0,
            "CommentCount": 0,
            "ContentLicense": "CC BY-SA 2.5"}    
        db.Posts.insert_one(post)  
    # for uid not provided
    else:
        post = {
            "Id": ID,
            "PostTypeId": "2",
            "CreationDate": post_date,
            "Body": "<p>"+body+"</p>",
            "ParentId": qid,
            "Score": 0,
            "CommentCount": 0,
            "ContentLicense": "CC BY-SA 2.5"}    
        db.Posts.insert_one(post)        
    print("answer "+ID +" saved.")
def vote_posts(pid,uid,db):
    ID = 'v' + generateID(db.Votes)
    now = datetime.now()
    vote_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]    
    if (len(str(uid)) >0):#uid provided
        #check if already voted on this post
        if (db.Votes.find_one({"UserId": uid, "PostId": pid})):
            print("You have already voted on this post!")
        else:
            vote = {
                "Id": generateID(db.votes),
                "PostId": pid,
                "UserId": uid,
                "VoteTypeId": "2",
                "CreationDate": vote_date}    
            db.Votes.insert_one(vote)
            db.Posts.update_one( {"Id": pid}, {"$inc": {"Score": 1} } )
            print("vote "+ID+ " saved.")
    else:
        #uid not provided
        vote = {
            "Id": generateID(db.votes),
            "PostId": pid,
            "VoteTypeId": "2",
            "CreationDate": vote_date}    
        db.Votes.insert_one(vote)
        db.Posts.update_one( {"Id": pid}, {"$inc": {"Score": 1} } )
        print("vote "+ID+ " saved.")
def answer_list(qid,uid,db):
    posts=[]
    answers=[]
    accept=db.Posts.find_one({"PostTypeId": "1","Id": qid})
    #append accepted answer
    if 'AcceptedAnswerId' in accept:
        posts.append(db.Posts.find_one({"Id": accept['AcceptedAnswerId']}))
        acc=True
    else:
        acc=False
    #append other questions
    answers=db.Posts.find({"PostTypeId": "2",'ParentId': qid})
    for answer in answers:
        if answer not in posts:
            posts.append(answer)
    #show results
    print("select from",len(posts), "answers or enter 0 to get back to the main menu")
    #For each answer, display the first 80 characters of the body text (or the full text if it is of length 80 or less characters), the creation date, and the score. 

    if acc:
        print('*1->','['+posts[0]['Body'][:80]+']',posts[0]['CreationDate'],"Score:",posts[0]['Score'])
        for i in range(1,len(posts)):
            print(str(i+1)+'->','['+posts[i]['Body'][:80]+']',posts[i]['CreationDate'],"Score:",posts[i]['Score'])
    else:
        for i in range(len(posts)):
            print(str(i+1)+'->','['+posts[i]['Body'][:80]+']',posts[i]['CreationDate'],"Score:",posts[i]['Score'])
    sel=input(">")
    while (sel.isdigit()==False or int(sel)<0 or int(sel)>len(posts)):
        sel=input("invalid input. Please select from above index:\n>")
    sel=int(sel)
    sel-=1
    if sel == -1:
        pass
    else:
        for k in posts[sel].keys():
            print(k,':',posts[sel][k])
        print("Do you think this answer helps you? Enter a word starting with 'y' to vote; or anything else to go back to the menu,case insensitive.")
        vote=input(">")[0].lower()
        if vote=='y':
            vote_posts(qid,uid,db)
        else:
            pass