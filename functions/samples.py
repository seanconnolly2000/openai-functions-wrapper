import os
from typing import List
import requests  
import datetime
import random


def getNews(**kwargs) -> List:
    # free sign up at newsapi.org
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


def getWeather(**kwargs)->List:
     # free signup at weatherapi.com
    query_params = kwargs
    query_params['key'] =  os.environ.get("WEATHERAPI_KEY")
    query_params['aqi'] = 'no'
    query_params['alerts'] = 'no'

    url = os.environ.get("WEATHER_URL")
    try:
        res = requests.get(url, params=query_params)
        data = res.json()
        weather = {}
        if data["current"] != None:
            weather['current_condition'] = data['current']['condition']['text']
            weather['current_temp_f'] = data['current']['temp_f']
            weather['current_temp_c'] = data['current']['temp_c']
        return weather
    except:
        return None


def getCurrentUTCDateTime() -> str:
    return str(datetime.datetime.utcnow())

def getDogName() -> str:
    return random.choice(['Fido', 'Spot', 'Rover', 'Woof'])
   