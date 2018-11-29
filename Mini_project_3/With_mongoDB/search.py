'''

 Copyright 2018 Leyang Yu yly@bu.edu
 
 This uses python 3.* and DO NOT support python 2.*
 This project requires pymongo library, and it needs to connect to an existing mongodb database

'''
from pymongo import MongoClient
import pprint

# Setting up client of mongoDB
client = MongoClient()
client = MongoClient('localhost', 27017)

# Choose Pics as the working database, and put it into posts
db = client.Pics
posts = db.posts

# Define a function to find tags and print the twitter ID and the urls.
def find_tags_in_Twitter_ID():
    print("You chose to search a tag in database.")
    Tags = input("Please input the Tags you are looking for:")
    formal_ID = ''
    check = 0
    for post in posts.find({"tags": Tags}).sort('Twitter_ID'):
        check = 1
        ID = post.get('Twitter_ID', [])
        if(ID != formal_ID):
            formal_ID = ID
            print("*********************************************")
            print(ID,' has follwing pictures including tag ',Tags)
        print(post.get('link', []),' searched by ',post.get('User_name', []))
    print("*********************************************")
    if(check == 0):
        print("*********************************************")
        print("Sorry, there is no picture corresponding with this tag.")
        print("*********************************************")

def statistic():
    formal_ID = ''
    print("*********************************************")
    for post in posts.find().sort('Twitter_ID'):
        ID = post.get('Twitter_ID', [])
        if(ID != formal_ID):
            formal_ID = ID
            count = posts.count_documents({"Twitter_ID": ID})
            print("There is ",count," pictures downloaded from ",ID)
    print("*********************************************")
    

if __name__ == '__main__':
    # Calculate the number of vaild data in the database
    i=0
    for post in posts.find({"Vaild": 1}):
        i = i + 1

    # If there is vaild data, go on and search inside
    if(i != 0 ):
        print("There is ",i," vaild pictures in the database.")
        Flag = input("Do you want to search for a tag(T) or you want to check the statistics(S)?")
        if(Flag == 'T'):
            find_tags_in_Twitter_ID()
        else:
            if(Flag == 'S'):
                statistic()
            else:
                print("Please input `T` to search for a tag, or `S` to check the statistics. Please check your input and try again.")

    # If there is no vaild data, skip searching and report and error
    else:
        print("ERROR: There is no vaild data in the database, please try executing the main.py and try again.")
    print("Execute ends")