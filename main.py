import os
from dotenv import load_dotenv
from functions.chat import functions, function, property, PropertyType
from openaif import openaif
import json

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
    f.properties.add(property("sortBy",PropertyType.string, "Sort By item", False))
    functions_available_to_chatGPT[f.name] = f

    # returns the datetime in GMT
    f = function(name="getCurrentDateTime", description="Obtain the current UTC date and time.")
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
 
    # CHALLENGE: make 3 calls: getDogName, get Time (and switch it to Pacific), and get some news stories
    prompt = "Get my dogs name, tell me what time is it in PST, and give me some news stories about the US Economy."
    res = oai.user_request(prompt)
    print(res)

if __name__ == "__main__":
    main()
