# twitter-api

Created a python web application with flask which will enable any user to view their Twitter stream within the app and User can search, filter and sort tweets.

## Get twitter developer API

Create a developer console using this [link](https://developer.twitter.com/)

Once you created the account you will get the `API key` `API Secret Key` and `Bearer Token`

## Setup Guide

1. Clone the repository in your machine and go to your root directory
2. Install virtual environment
    ```python3 -m venv env```
3. Do source activate   
    ```source venv/bin/activate```
4. Run requirement.txt file
    ```pip install -r requirements.txt```
5. create `.env` file and add below variables with necessory values
    ```python
       APP_SETTINGS="config.DevelopmentConfig"
       SQLALCHEMY_DATABASE_URI=''
       TWITTER_BEARER_TOKEN=''
       TWITTER_BASE_URL=''```
