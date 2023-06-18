# openai-functions-wrapper

## ChatGPT can now execute your functions as needed!

### TL;DR: On June 13, 2023, OpenAI released chatGPT4 (and 3.5Turbo) version "0613".  This release allows the ChatCompletion API to make "function_calls." This means that when provided with a list of functions, ChatCompletion will decide what functions are required to be executed to fulfill the user's request.  


This functionality is still experimental and results can be unpredictable and unreliable, but it is a huge step forward in allowing OpenAI's LLMs to interact with the real world, from news, weather, and stock data, to company proprietary vector databases.  This project provides an example chaininig together 5 function calls at ChatCompletion's request without using langchain.

Hopefully, this project will help demystify the pipeline for executing multiple requests with OpenAI's chatcompletion.

Additionally, I've created function wrappers that allow you to create the format necessary for chatcompletion to request function execution and parameters. You can add a function to your function list with as little as a single line of code.  Here is an example of the code required to enable ChatCompletion to interact with a Pinecone database:

```
    f = function(name="getPineconeData", description="Company data pertaining only to health care plans, company policies, and employee roles.")
    f.properties.add(property("prompt",PropertyType.string, "The prompt to be used to query the vector database.  This must be in the form of a concise sentence.", True))
    f.properties.add(property("top",PropertyType.integer, "Records to be returned.", True, None, default=5))
```
Obviously, you need to add the code to get the data, but wiring up with ChatCompletion is easy - **It is that simple!!!**

For ChatCompletion to work effectively, you need to keep a running history of the session.  This is done in the openaif.py file.  This illustrates how to append your conversation to "messages" to make the chat pipeline and function information work correctly.  This also allows you to inject a "system" message (which alters the chat context, I'm not sure if it is for the best...).

## Setup 
1) Download this project
2) Create a python environment and install the requirements (in requirements.txt)
3) create a .env file with the environment variables (see below)
4) Get any API keys you might need (or adjust the user prompt to say something simple like "what is my dogs name and what time is it?")

## .env File
Create a .env file in the directory with the following (depending on what you'll be using):
```
OPENAI_APIKEY={get a key from OpenAI}

NEWSAPI_ORG_URL=https://newsapi.org/v2/everything
NEWSAPI_KEY={get a free key from newsapi.org}

WEATHER_URL=http://api.weatherapi.com/v1/current.json
WEATHERAPI_KEY={get a free key from weatherapi.com}

PINECONE_API_KEY={get a free key from pinecone.io}
PINECONE_ENV={the environment on your index - often something like asia-southeast1-gcp..}
PINECONE_INDEX_NAME={whatever you named your index}
SENTENCE_ENCODER={I used all-MiniLM-L6-v2, which was in the 
                  pinecone demos, but you can use whatever - 
                  needed for encoding sentences for pinecone queries}
```

## Pinecone:
If you're going to use pinecone, you'll need to create an index on pinecone and add encoded data.  You can look at my other project "azure-pinecone-openai-demo" for scripts that will upload azure's "Northwinds" employee dataset, or upload your own data!  If you do, remember to update your description of what is stored in your data so ChatCompletion comprehends when that function_call might be required.


## Usage / Results

In the example, I show how you can have chatGPT request data from multiple sources.  Based upon the following prompt:

**"What is my dog's name, tell me what time is it in PST, what is the weather like in London, and what sightseeing activities would you recommend for London this time of year?  Also please give me 5 articles on the US Economy from the last week.  Also are hearing aids included in my Northwinds Standard Healthcare Plan?"**

ChatGPT determines it needs to perform the following external calls:

1) getCurrentUTCDateTime - system function to obtain the UTC date.
2) getDogName - system function to return a random dog name. :-)
3) getWeather - to obtain the weather in London (this is a free api you can sign up for at weatherapi.com)-
4) getNews - to obtain 4 news articles on the US Economy (this is a free api you can sign up for at newsapi.org)
5) getPineconeData - this illustrates how chatGPT can format a query to an external vector database and return silo'd information (you can sign up for a free Pinecone database at Pinecone.io).

The result is as follows (failed to give me sightseeing tips, but did give me 6 citations from external data sources!):

```
  "message": {
        "role": "assistant",
        "content": "Your dog's name is Fido.\n\n
        
        The current time in PST is 8:20 AM.\n\n
        
        The weather in London is partly cloudy with a temperature of 23.0\u00b0C (73.4\u00b0F).\n\n
        
        Here are 5 articles on the US Economy from the last week:\n
        1. Title: \"On-Orbit Satellite Servicing, New Crew Capsules and Artificial Gravity: NASA's Latest Tech Initiative\"\n   
        Description: \"A new Blue Origin crewed spacecraft is in the works as part of a NASA collaboration 
        designed to advance the orbital economy, with the space agency lending its expertise to seven different 
        commercial partners.\"\n\n
        2. Title: \"Partial de-dollarization is possible, but China won't dethrone the greenback even if 
        it becomes the world's largest economy\"\n 
        Description: \"History suggests that dollar dominance could carry on well into the second half 
        of the 21st century, even if China's economy outpaces the US.\"\n\n
        3. Title: \"Federal Reserve officials announce pause in US interest-rate hikes\"\n   
        Description: \"Even with the pause, Fed officials suggest further increases may come depending on 
        how close the economy gets to 2% inflation target.\"\n\n
        4. Title: \"Forget de-dollarization - Argentina may adopt the greenback as its currency and 
        abandon the peso\"\n   
        Description: \"If Argentina adopts the greenback, it would become the biggest economy so far to 
        dollarize, according to Bloomberg.\"\n\n
        5. Title: \"The US economy is entering expansion, not recession, and investors fear they are missing 
        out, Fundstrat's Tom Lee says\"\n  
        Description: \"The US is entering a phase of economic expansion and not a recession, which means the 
        stock-market rally will become more broad-based, Fundstrat's Tom Lee has said.\"\n\n
        
        Regarding your question about hearing aids in your Northwinds Standard Healthcare Plan, the plan 
        covers routine hearing aid maintenance and repair, counseling and hearing aid evaluations. It also 
        covers up to $500 per ear for hearing aid accessories such as ear molds, batteries, and tubing. 
        However, the plan does not cover hearing care services provided by out-of-network providers. If 
        you choose to see an out-of-network provider, you will be responsible for the difference between 
        their charges and the allowed amount by the plan."
      },
      "finish_reason": "stop"
    }
    
```

One thing I found of interest was that chatGPT formed a sentence for the vector search:

```

  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "function_call": {
          "name": "getPineconeData",
          "arguments": "{\n  \"prompt\": \"Northwinds Standard Healthcare Plan hearing aids\"\n}"
        }
      },
      "finish_reason": "function_call"
    }
  ],
  "usage": {
    "prompt_tokens": 803,
    "completion_tokens": 24,
    "total_tokens": 827
  }
```
