import pymongo
from pymongo import MongoClient
import post_question
import search_question
import sys

def check_question(uid,db):
    #get all the match question count and average score
    result = db.Posts.aggregate( [
                            { "$match": {"PostTypeId": "1", "OwnerUserId": uid} },
                            { "$group": { "_id": uid, "Qcount": { "$sum": 1 }, "AvgScore": {"$avg": "$Score"} } } ] )    
    return result   
def check_answer(uid,db):
    #get all the math answer count and average score
    result = db.Posts.aggregate( [
                            { "$match": {"PostTypeId": "2", "OwnerUserId": uid} },
                            { "$group": { "_id": uid, "Acount": { "$sum": 1 }, "AvgScore": {"$avg": "$Score"} } } ] )    
    return result     
def vote(uid,db):
    #get total vote count
    result = db.Votes.aggregate( [
                            { "$match": {"UserId": uid} },
                            { "$group": { "_id": uid, "TotalVotes": {"$sum": 1} } } ] )        
    return result
    
def login(db):
    valid = False
    while not valid:
        print("Welcome to login page!")
        uid = input("Please enter userID(optional): ")
        if (len(str(uid)) >0):
            u1 = ({"OwnerUserId":uid})#in posts
            u2 = ({"UserId":uid})#in votes
            rst = db.Posts.find_one(u1)
            rst1 = db.Votes.find_one(u2)        
            if rst != None or rst1 !=None:
                questions = check_question(uid,db)
                answers = check_answer(uid,db)
                votes = vote(uid,db)
                print("Hello " +uid)       
                listQ = list(questions)
                listA = list(answers)
                listV = list(votes)
                #for user with uid provided, showing the information
                if listQ:
                    print("Your total question count is "+str(listQ[0]['Qcount'])+', average score is ' + str(listQ[0]['AvgScore'])+'.')
                if listA:
                    print("Your total answer count is "+str(listA[0]['Acount'])+', average score is ' + str(listA[0]['AvgScore'])+'.')
                if listV:
                    print("Your total votes count is "+ str(listV[0]['TotalVotes']))
                break
            else:
                a = input("User not exists.\nContinue without userID press c, re-enter userID press r > ")
                if a.lower() == 'c':
                    valid = True
                elif a.lower() == 'r':
                    continue
        else:
            break
    return uid

def login_page(db):
    quit = False
    uid = login(db)
    while not quit:
        option = input("Please choose from the following options:\n1->post a question\n2->search for a post\n3->show login page\n0->quit\n")
        if option == '1':
            post_question.post_question(uid,db)
        elif option == '2':
            search_question.search_question(db,uid)
        elif option == '0':
            print('Goodbye')
            quit = True
            sys.exit()
        elif option == '3':
            uid = login(db)
        else:
            print('Invalid input. Please choose from the options provided.')

def main():
    port = int(sys.argv[1]) 
    client = pymongo.MongoClient('localhost', port)     
    db = client["291db"]
    login_page(db)
main()