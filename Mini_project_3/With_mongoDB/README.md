# EC601_Mini_Project3

## 1.Installing and starting MongoDB server

1.1 Install MongoDB server.

Firstly, please check [this website](https://docs.mongodb.com/manual/administration/install-community/) and download the proper version according to your OS. After that, please start mongoDB service on your local computer.

## 2.Running main.py

2.1 Setting up main.py

Modify the program by inputting your key to the twitter API into the 20th row of main.py, and the direction of your fonts into the 31th row of the program.

2.2 Getting all the libraries

In the terminal, download all the libraries imported in the program. You can download pymongo, which is the connector to the mongoDB in python, from [this page](https://api.mongodb.com/python/current/installation.html)

2.3 Setting up Google authentication.

In the terminal, set up authentication for Google Cloud by using argue
```
export GOOGLE_APPLICATION_CREDITS="./YOUR CREDIT FILE"
```

2.4 Running main.py

In the same terminal as the step 2.3, run 'python3 main.py'. During the running of the program, you should input the Twitter account that you like to download pictures from and the number of tweets you want to go through.

## 3.Running search.py

3.1 Main function

This program is designed to help user search for a specific Tag, and print the url of the pictures that contains this tag.

3.2 How to run it

You can simply run this file using `python3 search.py`, and input the Tags you want as the program requires. It will print out the urls of the pictures that contains the tag you input.


## 4.Results of running

4.1 Outputs

The outputs of this program is a video that contains a brief description of the pictures, together with those pictures, with each picture and its description showing for 5 second. It should be in `output.mp4`.

4.2 Databases

This program can store the urls to the pictures and the description into a mongoDB database. The results is in jason-style and it looks like this:<\br>
```
{'_id': ObjectId('Id_Number'),
 'author': 'Your_name',
 'link': 'PIC_URL',
 'tags': ['TAGS']}

```

