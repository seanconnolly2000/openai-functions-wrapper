import os
from typing import List
import requests  
import datetime
import random
from .openaif import *


def getCurrentUTCDateTime() -> str:
    return str(datetime.datetime.utcnow())

def getDogName() -> str:
    return random.choice(['Fido', 'Spot', 'Rover', 'Woof', 'Snoopy'])

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


def getCurrentWeather(**kwargs)->List:
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


def getThreeDayForecast(**kwargs)->List:
    # free signup at weatherapi.com
    query_params = kwargs
    query_params['key'] =  os.environ.get("WEATHERAPI_KEY")
    query_params['days'] = '3'
    query_params['aqi'] = 'yes'
    query_params['alerts'] = 'yes'

    url = os.environ.get("3DAY_WEATHER_URL")
    try:
        res = requests.get(url, params=query_params)
        data = res.json()
        forecast = "The weather forecast for the next 3 days in {} is:\n".format(kwargs['q'])
        if data["forecast"] != None:
            for day in data['forecast']['forecastday']:
                forecast += "{}. {} with a maximum temperature of {} and a minimum temperature of {}. There is a {} chance of rain.\n".format(
                    day['date'], 
                    day['day']['condition']['text'], 
                    day['day']['maxtemp_f'], 
                    day['day']['mintemp_f'], 
                    day['day']['daily_chance_of_rain'])
        return forecast
    except:
        return None

# This is a fun one - allow chatGPT to send text to itself and make requests
# Not sure this would ever happen, but kind of fun to think about...
def askChatGPT(**kwargs)->str:
    question = kwargs['question'] if 'question' in kwargs else ''
    text = kwargs['text'] if 'text' in kwargs else ''
    temperature = kwargs['temperature'] if 'temperature' in kwargs else 0
    prompt = "QUESTION:"  + question + "\nTEXT:" + text
    openai_key = os.environ.get("OPENAI_APIKEY")
    oai = openaif(openai_key)
    oai.temperature = temperature
    return oai.user_request(prompt)

# if you don't plan to use Sendgrid for sending emails, comment out this section
# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# def sendEmail(**kwargs)->str:
#   to_email = kwargs['to_email'] if 'to_email' in kwargs else None 
#   subject = kwargs['subject'] if 'subject' in kwargs else None 
#   body = kwargs['body'] if 'body' in kwargs else None 

    # leave if chat doesn't provide email, subject, or body
    # if to_email == None or subject == None or body == None: return
     

    message = Mail(from_email=os.environ.get('SENDGRID_FROM_EMAIL'), to_emails=to_email, subject=subject, html_content=body)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        if response.status_code == 202:
            return "MESSAGE WAS SUCCESSFULLY SENT."
        else:
            return "MESSAGE MAY NOT HAVE BEEN SENT."
        #print(response.status_code)
        #print(response.body)
        #print(response.headers)
    except Exception as e:
        #print(e.message)
        return "MESSAGE FAILED TO SEND."


# If you don't plan to use Pinecone, comment out everything below:
# import pinecone
# from sentence_transformers import SentenceTransformer
# import torch

# Initialize Pinecone client and the Index, which will be passed to the chat approaches.
# def getPineconeData(**kwargs)->str:
#   prompt = kwargs['prompt']
#   top = kwargs['top'] if 'top' in kwargs else 5

#   index=os.environ.get('PINECONE_INDEX_NAME')
#   api_key=os.environ.get('PINECONE_API_KEY')
#   env=os.environ.get('PINECONE_ENV')
#   sentence_encoder = os.environ.get('SENTENCE_ENCODER') # example: all-MiniLM-L6-v2
#   pinecone.init(
#           api_key=api_key,
#           environment=env
#           )
#   pinecone_index = pinecone.Index(index)
#   device = 'cuda' if torch.cuda.is_available() else 'cpu'
#   encoder = SentenceTransformer( sentence_encoder, device=device)
#   query = encoder.encode(prompt).tolist()
#   matches = pinecone_index.query(query, top_k=top, include_metadata=True)
#   content = ''
#   for result in matches['matches']:
#       content += result['metadata']['content']
#   return content


