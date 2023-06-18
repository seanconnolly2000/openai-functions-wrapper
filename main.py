import os
from dotenv import load_dotenv
from functions.chat import functions, function, property, PropertyType
from openaif import openaif
import json

from functions.samples import getWeather

def main():
    load_dotenv()
    # You'll need to create a ".env" file with your credentials in the format:
    #OPENAI_APIKEY=sk-xxxxxxx
    #OTHER_ITEMS=xxxyyy

    functions_available_to_chatGPT = functions()

    #If you've used SQLCLient or OracleClient, this is similar.  You create your function, and add parameters.
    # Then you add your function to the "functions" dictionary object (a dictionary is used to allow subsequent function lookup)
    # Note: "default" on properties is not specified, however, it seems to help chatcompletion.
    f = function(name="getNews", description="News API function")
    f.properties.add(property("q",PropertyType.string, "Query to return news stories", True))
    f.properties.add(property("language",PropertyType.string, "Language of News", True, ["en", "es"], default="en"))
    f.properties.add(property("pageSize",PropertyType.integer, "Page Size", True, None, default=5))
    f.properties.add(property("from",PropertyType.string, "Optional Date of oldest article.", False))
    f.properties.add(property("to",PropertyType.string, "Optional Date of newest article.", False))
    functions_available_to_chatGPT[f.name] = f

    # Weather API (current weather - can be improved to include forecast)
    f = function(name="getWeather", description="Weather API function")
    f.properties.add(property("q",PropertyType.string, "Name of city to get weather", True))
    functions_available_to_chatGPT[f.name] = f

    # Pinecone vector database API (contains demo "company HR data" from Northwinds)
    # comment out if you are not using Pinecone.
    f = function(name="getPineconeData", description="Company data pertaining only to health care plans, company policies, and employee roles.")
    f.properties.add(property("prompt",PropertyType.string, "The prompt to be used to query the vector database.  This must be in the form of a concise sentence.", True))
    f.properties.add(property("top",PropertyType.integer, "Records to be returned.", True, None, default=5))
    functions_available_to_chatGPT[f.name] = f

    # Send Email
    # comment out if you are not using SendGrid.
    f = function(name="sendEmail", description="Send an email. Must include to_email, subject, and body properties.")
    f.properties.add(property("to_email",PropertyType.string, "The email recipient address in email format.", True))
    f.properties.add(property("subject",PropertyType.string, "The subject of the email.", True))
    f.properties.add(property("body",PropertyType.string, "The body of the email.", True))
    functions_available_to_chatGPT[f.name] = f

    # returns the datetime in GMT
    f = function(name="getCurrentUTCDateTime", description="Obtain the current UTC datetime.")
    functions_available_to_chatGPT[f.name] = f

    # returns a random dog's name
    f = function(name="getDogName", description="Obtain the dog's name")
    functions_available_to_chatGPT[f.name] = f

    #instantiate the llm with the functions in list format (.to_json())
    openai_key = os.environ.get("OPENAI_APIKEY")
    oai = openaif(openai_key, functions_available_to_chatGPT)
  

    # Feel free to experiment with the system role below.  In my experiments, this seems to cause problematic output including ignoring user 
    # instruction to convert to PST, and sending content through in the same responses that also request a function_call.
    # oai.set_chat_context("You are an extremly happy assistant.  Only include data from function calls in your responses. If you don't know something, say 'I don't know.'")
 
    # FUN CHALLENGE: make 4 calls: getDogName, getCurrentDateTime (and switch it to Pacific - not always accurate), getWeather, and get some news stories
    # Since I am asking it to get a little creative with sightseeing tips for London, I'm setting the temperature below to 1.
    oai.temperature = 1
    prompt = "What is my dog's name, tell me what time is it in PST, what is the weather like in London, and what sightseeing activities would you recommend for London this time of year?  Also please give me 5 articles on the US Economy from the last week.  Also are hearing aids included in my Northwinds Standard Healthcare Plan? Also email sean@broadworld.com and tell him I am running late for lunch."
    res = oai.user_request(prompt)
    print(res)

if __name__ == "__main__":
    main()
