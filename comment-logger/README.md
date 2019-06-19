# Comment Logger
- basic comment logger to sign-up, post comments, and get comments

## Requirements
- Register a user with 'name' and 'password'
- Encrypt password with salted password hashing
- Each user gets 10 tokens
- Store a sentence in db for a cost of 1 token
- Retrieve user's stored sentence from db for cost of 1 token

## API Chart
```console
Resource    Address     Protocol    Paramater           Responses
-----------------------------------------------------------------
Home        /           GET         username,           200, 'Hello World ... !'

Register    /sign-up    POST        username,           200 OK
                                    password

Store
sentence    /store      POST        username,           200 OK
                                    password,           301 out of tokens
                                    sentence            302 Invalid username, password

Retrieve    /get        GET         username,           200 OK
sentence                            password            301 out of tokens
                                                        302 Invalid username, password
```

## Displaying the App in Your Web-broswer
- view app in 'http://localhost:5000/' of web browswer
```console
$ docker-compose build
$ docker-compose up
```

## Viewing Contents of the Database
- view IMAGE=comment-logger_db and insert 'CONTAINER ID' below
```console
$ docker ps
$ winpty docker container exec -it [CONTAINER ID] bash
> root@2205f6ec005c:/# mongo
> show dbs
SentencesDatabase  0.000GB
admin              0.000GB
config             0.000GB
local              0.000GB
> use SentencesDatabase
switched to db SentencesDatabase
> show collections
Users
> db.Users.find()
[ now you can view your users if you have inserted any]
```
