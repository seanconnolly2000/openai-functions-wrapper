import argparse
import os
import json

from dotenv import load_dotenv
from functions.openaif import openaif
from functions.chat import functions, function, property, PropertyType
from functions.samples import (
    getCurrentWeather,
    getThreeDayForecast,
    getNews,
    getCurrentUTCDateTime,
)
from audio_output import (
    initialize_audio,
    tts_output,
)  # Import the necessary functions from audio_output.py


def main():
    load_dotenv()
    # You'll need to create a ".env" file with your credentials in the format:
    # OPENAI_APIKEY=sk-xxxxxxx
    # OTHER_ITEMS=xxxyyy
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--speak", action="store_true", help="Enable text-to-speech output"
    )
    args = parser.parse_args()

    # Initialize audio if --speak is specified
    engine = None
    if args.speak:
        engine = initialize_audio()

    functions_available_to_chatGPT = functions()

    # Hmmm -  Not sure about this one - hopefully others might have thoughts. Let ChatGPT ask itself questions.  I'm not sure it can do that unless prompted by a user.
    # One thing I've noticed is that it may be beneficial to pass the main oai's "messages" into this so it has context...
    f = function(
        name="askChatGPT",
        description="Use a Large Language Model (LLM) to perform analysis, summarization, or classification of text using ChatGPT.",
    )
    f.properties.add(
        property(
            "temperature",
            PropertyType.integer,
            "The temperature associated with the request: 0 for factual, up to 2 for very creative.",
            True,
        )
    )
    f.properties.add(
        property(
            "question",
            PropertyType.string,
            "What are you requesting be done with the text?",
            True,
        )
    )
    f.properties.add(
        property("text", PropertyType.string, "The text to be analyzed", True)
    )
    functions_available_to_chatGPT[f.name] = f

    # If you've used SQLCLient or OracleClient, this is similar.  You create your function, and add parameters.
    # Then you add your function to the "functions" dictionary object (a dictionary is used to allow subsequent function lookup)
    # Note: "default" on properties is not specified, however, it seems to help chatcompletion.
    f = function(name="getNews", description="News API function")
    f.properties.add(
        property("q", PropertyType.string, "Query to return news stories", True)
    )
    f.properties.add(
        property(
            "language",
            PropertyType.string,
            "Language of News",
            True,
            ["en", "es"],
            default="en",
        )
    )
    f.properties.add(
        property("pageSize", PropertyType.integer, "Page Size", True, None, default=5)
    )
    f.properties.add(
        property("from", PropertyType.string, "Optional Date of oldest article.", False)
    )
    f.properties.add(
        property("to", PropertyType.string, "Optional Date of newest article.", False)
    )
    functions_available_to_chatGPT[f.name] = f

    # Weather API (current weather - can be improved to include forecast)
    f = function(
        name="getCurrentWeather", description="Weather API function for current weather"
    )
    f.properties.add(
        property("q", PropertyType.string, "Name of city to get weather", True)
    )
    functions_available_to_chatGPT[f.name] = f

    # Weather API (3-day forecast)
    f = function(
        name="getThreeDayForecast",
        description="Retrieves the weather forecast for the next 3 days for a specific city.",
    )
    f.properties.add(
        property("q", PropertyType.string, "Name of city to get weather", True)
    )
    functions_available_to_chatGPT[f.name] = f

    # Pinecone vector database API (contains demo "company HR data" from Northwinds)
    # comment out if you are not using Pinecone.
    # f = function(name="getPineconeData", description="Company data pertaining only to health care plans, company policies, and employee roles.")
    # f.properties.add(property("prompt",PropertyType.string, "The prompt to be used to query the vector database.  This must be in the form of a concise sentence.", True))
    # f.properties.add(property("top",PropertyType.integer, "Records to be returned.", True, None, default=5))
    # functions_available_to_chatGPT[f.name] = f

    # Send Email
    # comment out if you are not using SendGrid.
    # f = function(name="sendEmail", description="Send an email. Must include to_email, subject, and body properties.")
    # f.properties.add(property("to_email",PropertyType.string, "The email recipient address in email format.", True))
    # f.properties.add(property("subject",PropertyType.string, "The subject of the email.", True))
    # f.properties.add(property("body",PropertyType.string, "The body of the email.", True))
    # functions_available_to_chatGPT[f.name] = f

    # returns the datetime in GMT
    f = function(
        name="getCurrentUTCDateTime", description="Obtain the current UTC datetime."
    )
    functions_available_to_chatGPT[f.name] = f

    # returns a random dog's name
    f = function(name="getDogName", description="Obtain the dog's name")
    functions_available_to_chatGPT[f.name] = f

    # instantiate the llm with the functions in list format (.to_json())
    openai_key = os.environ.get("OPENAI_APIKEY")
    oai = openaif(openai_key, functions_available_to_chatGPT)

    # Feel free to experiment with the system role below.  In my experiments, this seems to cause problematic output including ignoring user
    # instruction to convert to PST, and sending content through in the same responses that also request a function_call.
    # oai.set_chat_context("You are an extremely happy assistant.  Only include data from function calls in your responses. If you don't know something, say 'I don't know.'")

    # FUN CHALLENGE: make 5 calls: getDogName, getCurrentDateTime (and switch it to Eastern - not always accurate), getCurrentWeather, getThreeDayForecast, and get some news stories.
    # "What is my dog's name, tell me what time is it in EST, what is the weather like in Atlanta, what sightseeing activities would you recommend for Metro Atlanta this time of year, and also please give me 5 articles from Atlanta from the last couple days."
    # Since I am asking it to get a little creative with sightseeing tips for Atlanta, I'm setting the temperature below to 1.
    oai.temperature = 1

    # Contributor John was cool enough to add the recursive question input.
    while True:
        prompt = input("Enter your question ('cls' to reset chat, 'quit' to quit): ")
        if prompt.lower() == "quit":
            break
        if prompt.lower() == "cls":
            oai.clear_chat_session()
        else:
            res = oai.user_request(prompt)
            # Replace the degree symbol
            res = res.replace("\u00b0F", " degrees Fahrenheit").replace(
                "\u00b0C", " degrees Celcius"
            )
            print(res)

            # Speak the response if --speak is specified
            if args.speak:
                tts_output(engine, res)


if __name__ == "__main__":
    main()
