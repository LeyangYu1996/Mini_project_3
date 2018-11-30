
# EC601_Mini_Project3

## 1.Installing and starting MySQL server

1.1 Install MySQL server.

Firstly, please check [this website](https://dev.mysql.com/downloads/) and download the proper version according to your OS. After that, MySQL database server will automatically run on your local host.

## 2.Setting up username and password in your database.

2.1 Logging into MySQL as root user.

You can log into MySQL as root user by input `sudo mysql -u root` in terminal of Linux.

2.2 Setting up new user.

In MySQL, you can use `CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';` to create a new user, whose username is `username` and password is `password`.

## 3.Setting up a new database and Google credentials to run main program.

3.1 Setting up a new database with required data structure.

Simply run `create_DB.py`, input `1` when asked whether you need to setup a new database or you need to reset the existing database.

3.2 Setting up Google authentication.

In the terminal, set up authentication for Google Cloud by using argue
```
export GOOGLE_APPLICATION_CREDENTIALS="./YOUR_FILE.json"
```
## 4.Running main.py

4.1 Running main.py

In the same terminal as the step 3.2, run `python3 main.py`. During the running of the program, you should input the Twitter account that you like to download pictures from and the number of tweets you want to go through.

## 5.Running search.py

5.1 Main function

This program is designed to help user search for a specific Tag, and print the url of the pictures that contains this tag.

5.2 How to run it

You can simply run this file using `python3 search.py`, and input the Tags you want to search as the program requires. It will print out the urls of the pictures that contains the tag you input.

## 6.Running counting.py

6.1 Main function

This program is designed to help user know the basic data of this database, including the total number of pictures that is recorded and the number of pictures belongs to each twitter account.

6.2 How to run it

You can simply run this file using `python3 counting.py`.

## 7.Results of running

7.1 Outputs

The outputs of this program is a video that contains a brief description of the pictures, together with those pictures, with each picture and its description showing for 5 second. It should be in `output.mp4`.

7.2 Databases

This program can store the urls to the pictures and the description into a MySQL database. The database is called Pics and it contains 3 different tables: 

| table     | contents |
| --- | --- |
| `pics_info`      | `Pic_No`, `Screen_name`(Twitter_account), `pic_url`      |
| `tags` | `tags_no`, `tags`         |
| `pic_tags`     |  `Pic_No` and corresponding `tags`         |

