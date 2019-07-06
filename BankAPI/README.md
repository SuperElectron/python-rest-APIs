# A Simple Bank API
- a simple API that mimics simple banking behaviour


## Requirements
- Initialize the bank at '/register' with POST 'username = BANK'
- Register a user with 'name' and 'password'
- Encrypt password with salted password hashing
- Charge user $1 for each transaction!
- No charge for loans, but track the user's parameters 'own' and 'debt'


## API Chart
```console
Resource    Address     Protocol    Paramater       	Responses
-----------------------------------------------------------------
Home        /           GET         anything        	200 OK, return "Hello World ... !

Register    /register   POST        username,       	200 You successfully signed up for the API
user                                password		301 Invalid username, user already exists


Add	    /add	POST 	    username,		200 Amount added successfully to account
money				    password,		301 Invalid username
				    amount		302 Invalid password
							304 Must add positive amount

Transfer   /transfer	POST        username,		200 Amount added successfully to account
money				    password,		301 Invalid username
				    to,			302 Invalid password
				    amount		303 Insufficient funds
				    		        304 Must transfer a positive amount

Check	   /balance 	POST	    username,		200 OK
balance				    password		301 Invalid username
				    			303 Insufficient funds


Take	  /takeloan	POST        username,		200 Loan Added to Your Account
loan				    password,		301 Invalid username
				    amount		302 Invalid password
							304 Must borrow positive amount


Pay	 /payloan	POST	    username,		200 Loan Paid
loan				    password,		301 Invalid username
				    amount		302 Invalid password
							303 Insufficient funds
							304 Must pay a positive amount			
```

# Setting up the Environment
- ensure you are in '/BankAPI' directory
```console
$ python -m venv env
$ source env/Scripts/activate
```

# Requirements
*Docker must be installed and running!*
- https://docs.docker.com/docker-for-windows/install/


## Displaying the App in Your Web-broswer
- ensure you are in '/BankAPI' directory
```console
$ docker-compose build
$ docker-compose up
```
- view app in 'http://localhost:5000/' of web browswer


## Testing the Database with Postman
- ensure that docker-compose up has the application running
```console
1. go to https://www.getpostman.com/products to download postman for free
2. open postman and click 'import' on the top bar
3. choose import from link
4. https://www.getpostman.com/collections/214cca47ec449328ddd5
5. try 'home' to ensure it is up and running
6. go to 'register BANK' and initialize username "BANK" to open up the banking app
7. register two users, and test out the API functionality
```


## Viewing Contents of the Database
- view NAMES=mongodb and insert 'CONTAINER ID' below
```console
$ docker ps
$ winpty docker container exec -it [CONTAINER ID] bash
> root@2205f6ec005c:/# mongo
> show dbs
MoneyManagementDB       0.000GB
> use MoneyManagementDB
switched to db MoneyManagementDB
> show collections
Users
> db.Users.find()
[ now you can view your users if you have inserted any]
```


## Requirements for AWS EC2 Hosting
*AWS EC2 must be configured on YOUR account with a .pem file downloaded*
- type: Ubuntu Server 18.04 LTS (HVM), SSD Volume Type , 64-bit (x86)
- size: t2.micro 
- Security groups => inbound: {type: ssh, protocol: TCP, Port range: 22, source: custom: 0.0.0.0/0}
- Security groups => inbound: {type: all traffic, protocol: all, Port range: 0-65535, source: anywhere: 0.0.0.0/0, ::/0}
- take note of "publicDNS(IPv4)" once your ubuntu machine is up and running
```console 
$ chmod 400 ~/[path-to-file.pem]
$ ssh -i ~/[path-to-file.pem] [ubuntu@{publicDNS(IPv4)}]

- if prompted, enter 'yes' and you will be logged into the machine with the following in the console ...
- to generate an ssh key, take note of login credentials and that you may or may not require email for github
- you can press enter until generation is completed

ubuntu@ip-xxx-xx-xx-xx:~$ ssh-keygen -t rsa -b 4096 -C

OR 

ubuntu@ip-xxx-xx-xx-xx:~$ ssh-keygen -t rsa -b 4096 -C "your_email@gmail.com"

ubuntu@ip-xxx-xx-xx-xx:~$ ls -al ~/.ssh
ubuntu@ip-xxx-xx-xx-xx:~$ vim ~/.ssh/id_rsa.pub
- copy the contents, exit VIM, and go to github.com/settings/keys and create a new ssh key

ubuntu@ip-xxx-xx-xx-xx:~/$ git clone https://github.com/[username]/[repository_name_you_want_to_add] 
ubuntu@ip-xxx-xx-xx-xx:~/$ cd BankAPI

- now download "docker CE for Ubuntu" to the AWS EC2 ubuntu machine
*setup the repository*
ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo apt-get update

ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo apt-key fingerprint 0EBFCD88

ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

*install docker CE for Ubuntu*
ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo apt-get update
ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo apt-get install docker-ce docker-ce-cli containerd.io
ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo docker run hello-world

*install docker-compose on Linux*
ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo chmod +x /usr/local/bin/docker-compose

ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ docker-compose --version

*run the application in the EC2 Ubuntu instance*
ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ ls
[ db docker-compose.yml web ]

ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo docker-compose build

ubuntu@ip-xxx-xx-xx-xx:~/BankAPI$ sudo docker-compose up

```

## Postman for EC2 instance
- import: https://www.getpostman.com/collections/687b44983f1bb8f2153a
- note that you must configure a ssh key for your repo AND change the post/get addresses
- e.g. ec2-3-18-221-38.us-east-2.compute.amazonaws.com:5000/ is my instance
- and {publicDNS(IPv4)}.compute.amazonaws.com:5000/ is your instance

## Troubleshooting
- email me at matmccann@gmail.com for any questions, and I'll do my best to help and add troubleshooting items here
