# A Similarity API for NLP
- this API uses 'https://spacy.io/' natural language processing to give a statistical measure of similarity between two text strings.

## Requirements
- Register a user with 'name' and 'password'
- Encrypt password with salted password hashing
- Each user gets 3 tokens
- Display similarity stats from text string comparison of "text1" to "text2" for a cost of 1 token
- Administrative ability to 'refill tokens' to user may use API more

## API Chart
```console
Resource        Address     Protocol    Paramater           Responses
-----------------------------------------------------------------
Register        /register   POST        username,           200 OK, return "Hello World ... !

Register        /register   POST        username,           200 OK
a new user                              password            301 Invalid Username: the username already exists


Detect          /detect     POST        username,           200 OK, return Similarity
similarity                              password,           301 Invalid username
of docs                                 sentence            302 Invalid password
                                                            303 Out of tokens

Refill          /refill     POST        username,           200 OK
                                        password            301 Invalid username
                                                            304 Invalid admin password
```

# Setting up the Environment
- ensure you are in '/NLP-Similarity-API' directory
```console
$ python venv env
$ source env/Scripts/activate
```

# Requirements
*Docker must be installed and running!*
- https://docs.docker.com/docker-for-windows/install/

## Displaying the App in Your Web-broswer
- view app in 'http://localhost:5000/' of web browswer
- ensure you are in '/NLP-Similarity-API' directory
```console
$ docker-compose build
$ docker-compose up
```

## Testing the Database with Postman
- ensure that docker-compose up has the application running
```console
1. go to https://www.getpostman.com/products to download postman for free
2. open postman and click 'import' on the top bar
3. choose import from link
4. https://www.getpostman.com/collections/c66d18578ac01cbbcb23
5. try 'home' to ensure it is up and running and then register yourself to the API!
```

## Viewing Contents of the Database
- view NAMES=mongodb and insert 'CONTAINER ID' below
```console
$ docker ps
$ winpty docker container exec -it [CONTAINER ID] bash
> root@2205f6ec005c:/# mongo
> show dbs
SimilarityDB       0.000GB
> use SimilarityDB
switched to db SimilarityDB
> show collections
Users
> db.Users.find()
[ now you can view your users if you have inserted any]
```

## Natural Language Processing Model
- refer to https://spacy.io/models/en for more information


## Troubleshooting
- web/app.py has line ending LF
- ERROR: "driver failed programming external connectivity on endpoint" may require you to restart docker
- in the above error, follow the useful commands 'system prune' and 'volume prune'
- still not working? try docker-compose build --no-cache to ensure you aren't building off previous images
- email me at matmccann@gmail.com for any questions, and I'll do my best to help.
