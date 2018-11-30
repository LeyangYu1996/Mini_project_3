'''
 Copyright 2018 Leyang Yu yly@bu.edu

 This uses python 3.* and DO NOT support python 2.*
 This project requires tweepy, urllib, google.cloud, PILLOW and ffmpeg libraries.
 This project uses MySQL database to store picture information. 
 Setting up authentication for Google Cloud is REQUIRED before running this program.
'''
import tweepy
#Ref:https://github.com/tweepy/tweepy
from urllib import request
import os
import io
from google.cloud import vision
from google.cloud.vision import types
#Ref:https://cloud.google.com/vision/docs/libraries#client-libraries-install-python
from PIL import Image, ImageDraw, ImageFont
#Ref:https://pillow.readthedocs.io/en/5.2.x/#
import ffmpeg
#Ref:https://github.com/kkroening/ffmpeg-python
import mysql.connector
from mysql.connector import errorcode

# Set up twitter credentials
consumer_key = YOUR_KEY
consumer_secret = YOUR_KEY
access_key = YOUR_KEY
access_secret = YOUR_KEY

# Please input your database user_name and password here.
DB_USER = 'user'
DB_PASSWORD = 'password'

# Input the direction of your fonts here
fonts = './FONTs.ttf'

def download_tweets(Name):
    # Put the screen name into this part
    screenname = Name

    # Use the keys and secrets to access to the api
    auth = tweepy.OAuthHandler( consumer_key, consumer_secret)
    auth.set_access_token( access_key, access_secret)
    api = tweepy.API(auth)

	# Download first set of status
    num = input('please input the number of tweets you want to go through(max=200)')
    try:
        num_pic = int(num)
    except:
        print('please type in the number of the tweets, ONLY integers below 200 is accepted.')
        return 0
    print('Getting tweets')
    try:
        public_tweets = api.user_timeline(screen_name = screenname, count = num_pic)
    except:
        print('Tweeter API is not accessable or the name you put in is wrong.')
        return 0

    # Connect to the database and create a cursor
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,database='Pics')
    cursor = cnx.cursor()

    # Check if there is no tweets downloaded
    if(len(public_tweets) == 0):
        print('No Tweets found')
        return 0
    else:
	    # Get the urls of all pictures and save them into a list
        picurl = set()
        for status in public_tweets:
            media = status.entities.get('media', [])
            if(len(media) > 0):
                picurl.add(media[0]['media_url'])
        # Check if NO media files were found
        if(len(picurl) == 0):
            print('No Pictures Found')
            return 0
	    # If there is media files, use urltrieve to download the urls
        else:
            if os.path.exists('./PICS') == False:
                os.makedirs('./PICS')
            i=0
            print('Downloading Pictures')

            # Setup the cursor 
            add_pic = ("INSERT IGNORE INTO pics_info "
                       "(Pic_No, Screen_name, pic_url) "
                       "VALUES (%s, %s, %s)")

            for media_file in picurl:
                i=i+1
                # Get the max of Pic_No
                cursor.execute("SELECT MAX(Pic_No) FROM pics_info")
                last_Pic_No = cursor.fetchall()[0][0]
                if last_Pic_No == None:
                    last_Pic_No = 0
                # Add pic_info into Pics
                data_pic = (last_Pic_No+1, screenname, media_file)
                cursor.execute(add_pic, data_pic)
                # Download pics
                path_name = os.path.join('./PICS/', str(i)+'.jpg')
                request.urlretrieve(media_file, path_name)
            print('***************************')
            print(str(i)+' pictures downloaded')
            print('***************************')

            cnx.commit()
            cursor.close()
            cnx.close()
            return 1



def get_labels(Start_Pic_No):
    # Setup to access to the Google Vision API
    # os.system cannot upload the credential correctly, so FOR NOW it is necessary to run this in shell
    client = vision.ImageAnnotatorClient()
    i = 1
    print('Getting labels from google and printing labels on it')
    while(1):
        # Check if there are pictures inside the folder
        if os.path.exists('./PICS/'+str(i)+'.jpg') == True:
            file_name = os.path.join(os.path.dirname(__file__),'./PICS/'+str(i)+'.jpg')
            # Read the pictures and get ready to push it to Google
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()
            
            image = types.Image(content=content)
            
            # Get the labels from Google Vision
            try:
                response = client.label_detection(image=image)
                labels = response.label_annotations
            except:
                print('Google API is not accessable at this time, please check your creditional or try again later.')
                return 0

            # Connect to the database and create a cursor
            cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,database='Pics')
            cursor = cnx.cursor()

            # Setup the cursor 
            add_tags = ("INSERT IGNORE INTO tags "
                       "(tags_no, tags) "
                       "VALUES (%s, %s)")
            add_pic_tags = ("INSERT IGNORE INTO pic_tags "
                       "(Pic_No, tags_no) "
                       "VALUES (%s, %s)")

            # Setup PILLOW to put labels into the picture
            # Input the direction of your fonts here
            im = Image.open('./PICS/'+str(i)+'.jpg')
            draw = ImageDraw.Draw(im)
            myfont = ImageFont.truetype(fonts, size=35)
            # As a result, the FONTs.ttf should be copied to the same folders
            fillcolor = 'red'
            # Put label into the picture
            m = 0
            for label in labels:
                m = m + 1
                # Put tags into database, and put the connections between pic and tags into database
                cursor.execute("SELECT MAX(tags_no) FROM tags")
                tags_start_id = cursor.fetchall()[0][0]
                if tags_start_id == None:
                    tags_start_id = 0
                data_tags = (tags_start_id+1, label.description)
                cursor.execute(add_tags, data_tags)
                cnx.commit()
                cursor.execute("SELECT tags_no FROM tags WHERE tags = '"+label.description+"'")
                tags_no = cursor.fetchall()[0][0]
                data_pic_tags = (Start_Pic_No + i, tags_no)
                cursor.execute(add_pic_tags, data_pic_tags)
                cnx.commit()                
                if m <= 2:
                	# Only draw 3 tags into the picture
                    draw.text((40, 40*m), label.description, font=myfont, fill=fillcolor)
            im.save('./PICS/'+str(i)+'.jpg', 'JPEG')
            print('Printing labels on the '+str(i)+'th Picture')
            i = i + 1
        # Print the total number of the pictures
        else:
            print('***************************')
            print(str(i - 1)+' pictures completed')
            print('***************************')
            cursor.close()
            cnx.close()
            return 1
            break

def Get_DB_Start():
    # Get the start of the Pic_info table, in order to connect Pics and tags

    # Connect to the database and create a cursor
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,database='Pics')
    cursor = cnx.cursor()    

    cursor.execute("SELECT MAX(Pic_No) FROM pics_info")
    last_Pic_No = cursor.fetchall()[0][0]
    if last_Pic_No == None:
        last_Pic_No = 0
    return last_Pic_No

def Put_to_video():
    # Use ffmpeg to convert the pictures into a video
    try:
        os.system("ffmpeg -framerate 1/5 -pattern_type glob -i './PICS/*.jpg' -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4")
    except:
        print('ffmpeg fails')

def Delete_Files():
    # Delete the pictures downloaded in order to save storage space of the computer
    i = 1
    while(1):
        # Check if the path has pictures inside
        if os.path.exists('./PICS/'+str(i)+'.jpg'):
            os.remove('./PICS/'+str(i)+'.jpg')
            i = i + 1
        else:
            break
    os.removedirs('./PICS')

if __name__ == '__main__':
    Name = input("input Screen Name :")
    Start_Pic_No = Get_DB_Start()
    Checker = download_tweets(Name)
    if Checker == 1:
        if (get_labels(Start_Pic_No)):
            Put_to_video()
            Delete_Files()
            print('***************************')
            print('Output is Complete')
            print('***************************')
    else:
        print('Progress failed, please check your input and try again.')

