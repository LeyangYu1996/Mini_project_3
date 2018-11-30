'''

 Copyright 2018 Leyang Yu yly@bu.edu

 This uses python 3.* and DO NOT support python 2.*
 This project requires tweepy, urllib, google.cloud, PILLOW and ffmpeg libraries.
 This project uses MySQL database to store picture information. 
 Setting up authentication for Google Cloud is REQUIRED before running this program.
'''
import mysql.connector
from mysql.connector import errorcode

# Please input your database user_name and password here.
DB_USER = 'user'
DB_PASSWORD = 'password'

# Input the tag which user is looking for.
tag = input("Please enter the tag you would like to search: \n")
cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,database='Pics')
cursor = cnx.cursor()

try:
    # Get the tag_no of tags.
    cursor.execute("SELECT tags_no FROM tags WHERE tags = '"+tag+"'")
    tags_no = cursor.fetchall()[0][0]
except:
    print("Sorry, no picture corresponds to this tag is found. Please try again.")
    cursor.close()
    cnx.close()
    exit()

# Get the Pic_No of the pictures that contains this tag.
cursor.execute("SELECT Pic_No FROM pic_tags WHERE tags_no = '"+str(tags_no)+"'")
Pic_Nos = cursor.fetchall()

# Get the picture url that corresponding to the Pic_No, and print the urls of picture that contain this tag.
formal_sn = '0'
for Pic_No in Pic_Nos:
    cursor.execute("SELECT Screen_name FROM pics_info WHERE Pic_No = '"+str(Pic_No[0])+"'")
    Screen_name = cursor.fetchall()[0][0]
    cursor.execute("SELECT pic_url FROM pics_info WHERE Pic_No = '"+str(Pic_No[0])+"'")
    pic_url = cursor.fetchall()[0][0]
    if(Screen_name!=formal_sn):
        formal_sn = Screen_name
        print('***********************************************************')
        print("Following pictures from ",Screen_name,' have ',tag,' in it:')
    print(pic_url)
cursor.close()
cnx.close()