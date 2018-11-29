import mysql.connector
from mysql.connector import errorcode

tag = input("Please enter the tag you would like to search: \n")
cnx = mysql.connector.connect(user='user', password='password',database='Pics')
cursor = cnx.cursor()

cursor.execute("SELECT tags_no FROM tags WHERE tags = '"+tag+"'")
tags_no = cursor.fetchall()[0][0]

cursor.execute("SELECT Pic_No FROM pic_tags WHERE tags_no = '"+str(tags_no)+"'")
Pic_Nos = cursor.fetchall()

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