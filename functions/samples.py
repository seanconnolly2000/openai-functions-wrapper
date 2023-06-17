import os
from typing import List
import requests  
import datetime
import random


def getNews(**kwargs) -> List:
    query_params = kwargs
    query_params['apiKey'] =  os.environ.get("NEWSAPI_KEY")
    url = os.environ.get("NEWSAPI_ORG_URL")

    # fetching data in json format
    try:
        res = requests.get(url, params=query_params)
        data = res.json()
        news = []
        if data["articles"] != None:
            for article in data["articles"]:
                news.append({'title': article['title'], 'description': article['description']})
        return news
    except:
        return None


def getCurrentDateTime() -> str:
    return str(datetime.datetime.utcnow())

def getDogName() -> str:
    return random.choice(['Fido', 'Spot', 'Rover', 'Woof'])
   