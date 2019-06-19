# Flask-tutorial-2
- simple flask application to add numbers with docker


## SETTING UP THE VIRUTAL ENVIRONMENT
##### Create python virtual environment in Flask-tutorial-1
```console
$ python -m venv env
```


##### Activate the Vitual environment
```console
$ source env/Scripts/activate
```


##### Run the application
```console
$ export FLASK_APP=app.py
$ docker-compose build
$ docker-compose up

- Default home page for available in 'http://localhost:5000/' of web browswer
```