# An Image Classification API based on Tensorflow
- this API uses tensorflow to classify images based on the Inception model trained on ImageNet 2012 Challenge data set.

## Requirements
- Register a user with 'name' and 'password'
- Encrypt password with salted password hashing
- Each user gets 3 tokens
- Display classification stats from any web based url of a picture for a cost of 1 token
- Administrative ability to 'refill tokens' to user may use API more

## API Chart
```console
Resource        Address     Protocol    Paramater           Responses
-----------------------------------------------------------------
Home            /           GET         anything            200 OK, return "Hello World ... !

Register        /register   POST        username,           200 OK
a new user                              password            301 Invalid Username: the username already exists


Classify        /detect     POST        username,           200 OK, return {Classification}
an image                                password,           301 Invalid username
                                        url                 302 Invalid password
                                                            303 Out of tokens

Refill          /refill     POST        username,           200 OK
                                        admin_pw,           301 Invalid username
                                        amount              304 Invalid admin password
```

# Setting up the Environment
- ensure you are in the '/Tensorflow-ImageClassification' directory
```console
$ python -m venv env
$ source env/Scripts/activate
```

# Requirements
*Docker must be installed and running!*
- https://docs.docker.com/docker-for-windows/install/

## Displaying the App in Your Web-broswer
- view app in 'http://localhost:5000/' of web browswer
- ensure you are in '/Tensorflow-ImageClassification' directory
```console
$ docker-compose build
$ docker-compose up
```

## Testing the Database with Postman
- ensure that 'docker-compose up' has the application running
```console
1. go to https://www.getpostman.com/products to download postman for free
2. open postman and click 'import' on the top bar
3. choose import from link
4. https://www.getpostman.com/collections/de5c5651a9763f3d8f84
5. try 'home' to ensure it is up and running and then register yourself to the API!
```

## Viewing Contents of the Database
- view NAMES=mongodb and insert 'CONTAINER ID' below
```console
$ docker ps
$ winpty docker container exec -it [CONTAINER ID] bash
> root@2205f6ec005c:/# mongo
> show dbs
IRG       0.000GB
> use IRG
switched to db IRG
> show collections
Users
> db.Users.find()
[ now you can view your users if you have inserted any]
```

## Natural Language Processing Model
- refer to https://spacy.io/models/en for more information

## Random Docker Functions
- A handful of docker CLI functions that are extremely helpful when working. \
```console
*Stop all containers and remove network
$ docker-compose down
*Show all runnning containers
$ docker ps
*ID's are found in the previous line
$ docekr logs <id>
*Show all running and stopped containers
$ docker ps -a
*Remove all stopped containers
$ docker system prune
*Remove all stopped networks
$ docker network prune
*Remove all stopped/detached volume
$ docker volume prune
*delete all volumes and images
$ docker rm $(docker ps -aq) && docker rmi $(docker images -q)
```

## Troubleshooting
- web/app.py has line ending LF
- ERROR: "driver failed programming external connectivity on endpoint" may require you to restart docker
- in the above error, follow the useful commands 'system prune' and 'volume prune'
- still not working? try docker-compose build --no-cache to ensure you aren't building off previous images
- email me at matmccann@gmail.com for any questions, and I'll do my best to help.
