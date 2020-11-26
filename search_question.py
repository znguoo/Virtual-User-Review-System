from datetime import datetime
import time
import re
import random
import pymongo
import post_action
from pymongo import MongoClient
def search_question(db,uid):
    #user provide one or more keywords.
    keys=[]
    keys=input("Please enter key word(s) you are looking for,split with white spaces:\n>").lower().split()
    print("keys:",keys)
    #keywords could in title, body or tags(case-insensitive)
    posts=[]
    for key in keys:
        #add all posts with keywords in title
        titles = db.Posts.find({'Title':re.compile(key, re.IGNORECASE),"PostTypeId":"1"})
        for post in titles:
            if post not in posts:
                posts.append(post)      
        #add all posts with keywords in body
        bodys = db.Posts.find({'Body':re.compile(key, re.IGNORECASE),"PostTypeId":"1"})
        for post in bodys:
            if post not in posts:
                posts.append(post)          
        #add all posts with keywords in tag
        tags = db.Posts.find({'Tags':re.compile(key, re.IGNORECASE),"PostTypeId":"1"})
        for post in tags:
            if post not in posts:
                posts.append(post)  
        #display results for selection
        print("select from",len(posts), "questions or enter 0 to get back to the main menu")
        for i in range(len(posts)):
            print(str(i+1)+":","["+posts[i]['Title']+"]",posts[i]['CreationDate'],"Score:",posts[i]['Score'],"Answers:",posts[i]['AnswerCount'])
        #select from question and view count++
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
            db.Posts.update_one( {"Id": posts[sel]["Id"]}, {"$inc": {"ViewCount": 1} } )
            print("="*15)
            #Qestion action
            print("You can now perform Question action for","["+posts[sel]['Title']+"]. Select from 1 to 3 or 0 to show main menu")
            print("1.Answer")
            print("2.List answers")
            print("3.Vote")
            act=input(">")
            while act not in ['1','2','3','0']:
                act=input("Invalid input. Please select from 1 2 3\n>")
            if act=='1':
                post_action.answer_question(posts[sel]['Id'],uid, db)
            elif act=='2':
                post_action.answer_list(posts[sel]['Id'],uid,db)
            elif act=='3':
                post_action.vote_posts(posts[sel]['Id'],uid,db)
            else:
                pass
