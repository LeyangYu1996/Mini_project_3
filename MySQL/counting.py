import mysql.connector

# Connect to the database and create a cursor
cnx = mysql.connector.connect(user='user', password='password',database='Pics')
cursor = cnx.cursor()

cursor.execute("SELECT tags_no FROM tags")
tags_no_all = cursor.fetchall()
tags_no_usage_max = 0
tags_no_max = set()
for tags_no in tags_no_all:
    cursor.execute("SELECT COUNT(*) FROM pic_tags WHERE tags_no = '"+str(tags_no[0])+"'")
    tags_no_usage = cursor.fetchall()[0][0]
    if(tags_no_usage > tags_no_usage_max):
        tags_no_usage_max = tags_no_usage
        tags_no_max = set()
    if(tags_no_usage == tags_no_usage_max):
        tags_no_max.add(str(tags_no[0]))

if(len(tags_no_max)==1):
    for tags_no in tags_no_max:
        cursor.execute("SELECT tags FROM tags WHERE tags_no = '"+tags_no+"'")
        tags_no_print = cursor.fetchall()[0][0]
        print("The tag ",tags_no_print," is the most used tag, it appeared ",tags_no_usage_max,' times.')
else:
    print("The following tags are most used tags, which appeared ",tags_no_usage_max,' times.')
    for tags_no in tags_no_max:
        cursor.execute("SELECT tags FROM tags WHERE tags_no = '"+tags_no+"'")
        print(cursor.fetchall()[0][0])

Screen_name_set = set()
cursor.execute("SELECT Screen_name FROM pics_info")
Screen_name_all = cursor.fetchall()
for Screen_name in Screen_name_all:
    Screen_name_set.add(Screen_name[0])

for Screen_name in Screen_name_set:
    cursor.execute("SELECT COUNT(*) FROM pics_info WHERE Screen_name = '"+Screen_name+"'")
    count = cursor.fetchall()[0][0]
    print('You have downloaded ',count,' pictures from ',Screen_name)

cursor.close()
cnx.close()


