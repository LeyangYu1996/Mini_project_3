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
def find_tags_in_Twitter_ID(Tags):
    formal_ID = ''
    for post in posts.find({"tags": Tags}).sort('Twitter_ID'):
        ID = post.get('Twitter_ID', [])
        if(ID != formal_ID):
            formal_ID = ID
            print("*********************************************")
            print(ID,' has follwing pictures including tag ',Tags)
        print(post.get('link', []),' searched by ',post.get('User_name', []))

if __name__ == '__main__':
    # Calculate the number of vaild data in the database
    i=0
    for post in posts.find({"Vaild": 1}):
        i = i + 1

    # If there is vaild data, go on and search inside
    if(i != 0 ):
        print("There is ",i," vaild pictures in the database.")
        Tags = input("Please input the Tags you are looking for:")
        find_tags_in_Twitter_ID(Tags)

    # If there is no vaild data, skip searching and report and error
    else:
        print("ERROR: There is no vaild data in the database, please try executing the main.py and try again.")