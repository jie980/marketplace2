# McGill C2C Marketplace
A marketplace project implemented with django and JavaScript in Python. McGill University Comp 307 final project, 2020 winter.
## LocalHost 
```
The webpage is hosted on 127.0.0.1:8000/app
```
## Group members
```
Jane  Gao  260750643
Kehan Li   260765991
Jie   Min  260846867
```
### Prerequisites
```
python 3.6 or above
Django 3 
channels==1.0.2 or above
asgi_redis==1.0.0 or above
```
### Installing
You need to install following things in order to run our program.
(Mac, Windows and linux might be different)
```
1.Install libssl-dev (sudo apt-get install libssl-dev)
2.python3 –m pip install -U channels
3.sudo apt-get install redis-server
4.python3 -m pip install channels_redis
5.pip3 install pillow
```
And migrate (the example below is on windows)
```
python runserver.py makemigrations
python runserver.py migrate
```

## Running the tests
The commands for running the tests
```
python3 manage.py test
```
## Built With

* [Django](https://www.djangoproject.com/) - The backend used
* [JavaScript](https://www.javascript.com/) - The Front end used
* [Bootstrap](https://getbootstrap.com/docs/4.4/getting-started/) - The Front end used
* [Redis](https://redis.io/) - The Data structure used

## Thank you and stay healthy!
