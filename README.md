## Table of contents
* [General info](#general-info)
* [Functionality](#functionality)
* [Technologies](#technologies)
* [Style conventions](#style-conventions)
* [Setup](#setup)

## General info
The app introduces an API with events in the following structure (JSON requests):
- ``user_id``: <INT, REQUIRED>;
- ``app_name``: <STRING, REQUIRED>;
- ``event_action``: <STRING, NULLABLE>;
- ``event_category``: <STRING, REQUIRED>;
- ``event_value``: <INT, NULLABLE>
Gathered data should be stored in Data Lake in the most optimal way in terms of API
performance.
  

## Functionality

### Project has been implemented in 2 versions:
- V1: with Docker compose + SQS + Data Lake partition by `app_name`
- V2: with local run `python3 main_v2.py` and RequestHolder class as quick & dirty implementation of messages holder, without partitioning in data lake 
  


Send POST requests to: 
```
http://localhost:5000/track
```


## Technologies
Project is created with:
* boto3==1.26.53
* black==20.8b1
* flask==2.2.2
* pandas==1.5.3
* flask_limiter==3.1.0
* pyarrow==10.0.1


## Style conventions
For code conventions used Black library.

## Setup
To run this project locally, make the following:

```
$ git clone https://github.com/lesnata/flask-api.git
$ cd flask-api
$ virtualenv venv
$ source venv/bin/activate
```

Fill in `.env` details with your AWS creds:
```
AWS_ACCESS_KEY_ID=SUPER_SECRET_ID
AWS_SECRET_ACCESS_KEY=SUPER_SECRET_PASS
AWS_REGION=us-east-1
```

Run docker compose:
```
docker compose build
docker compose up
```


Example of JSON body request:
```
{
    "user_id": "434",
    "app_name": "CleanMyMac",
    "event_action": "click",
    "event_category": "app",
    "event_value": 2
}
```

