# Big Fat Festival Ticketing API

## Features
Create a User his information, creates a QR Ticket for them and saves the information for event management team to give out passes and check the passes

* <a href='https://flask-dynamo.readthedocs.io/en/latest/quickstart.html'>Mongo-Flask DB</a>

* <a href='https://github.com/deejungx/flask-cognito-extended.git'>Cognito Flask User Authentification</a>

* <a href='https://docs.mongoengine.org/tutorial.html'>Mongoengine Documentation</a>

## What this Repo Contains?

*  Flask-Mongo Restful API  
 
*  Flask-Congito Auth Routes

*  Sample Postman Export


## How to run the Sample code

To initiall setup the enviroment 

```
virtualenv venv
cd venv/Script
activate
cd ..
cd ..
pip3 install -r requirements.txt
```

To run the API

```
python wsgi.py

```

## Test the API

Setup Postman and import the collection. Afterwards add the bearer (token) in the header of the request in postman for routes that only accept registered users else the routes won't work

