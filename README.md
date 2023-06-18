# openai-functions-wrapper

## ChatGPT can now execute your functions (including accessing your database) as needed, and even send emails out on your behalf!

### TL;DR: On June 13, 2023, OpenAI released chatGPT4 (and 3.5Turbo) version "0613".  This release allows the ChatCompletion API to make "function_calls." This means that when provided with a list of functions, ChatCompletion will decide what functions are required to be executed to fulfill the user's request.  


This functionality is still experimental and results can be unpredictable and unreliable, but it is a huge step forward in allowing OpenAI's LLMs to interact with the real world, from news, weather, and stock data, to company proprietary vector databases.  This project provides an example chaininig together 5 function calls at ChatCompletion's request without using langchain.

Hopefully, this project will help demystify the pipeline for executing multiple requests with OpenAI's chatcompletion.

Additionally, I've created function wrappers that allow you to create the format necessary for chatcompletion to request function execution and parameters. You can add a function to your function list with as little as a single line of code.  Here is an example of the code required to enable ChatCompletion to interact with a Pinecone database:

```
    f = function(name="getPineconeData", description="Company data pertaining only to health care plans, company policies, and employee roles.")
    f.properties.add(property("prompt",PropertyType.string, "The prompt to be used to query the vector database.  This must be in the form of a concise sentence.", True))
    f.properties.add(property("top",PropertyType.integer, "Records to be returned.", True, None, default=5))
```
Obviously, you need to add the code to get the data, but **wiring up function definitions with ChatCompletion is now super easy!**

For ChatCompletion to work effectively, you need to keep a running history of the session.  This is done in the openaif.py file.  This illustrates how to append your conversation to "messages" to make the chat pipeline and function information work correctly.  This also allows you to inject a "system" message (which alters the chat context, I'm not sure if it is for the best...).

## Setup 
1) Download this project
2) Create a python environment and install the requirements (in requirements.txt)
3) create a .env file with the environment variables (see below)
4) Get any API keys you might need (or adjust the user prompt to say something simple like "what is my dogs name and what time is it?" which doesn't require any external api calls.)

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

SENDGRID_FROM_EMAIL=xxx@yyy.com
SENDGRID_API_KEY={get a free api key from sendgrid.com - it looks like you do need to add a credit card to activate, however.}

              
```

## Pinecone:
If you're going to use pinecone, you'll need to create an index on pinecone and add encoded data.  You can look at my other project "azure-pinecone-openai-demo" for scripts that will upload azure's "Northwinds" employee dataset, or upload your own data.  If you use your own data, remember to update the description of what is stored in your data so ChatCompletion can comprehend when that function_call might be required.


## Usage / Results

In the example, I show how you can have chatGPT request data from multiple sources.  Based upon the following prompt:

**"What is my dog's name, tell me what time is it in PST, what is the weather like in London, and what sightseeing activities would you recommend for London this time of year?  Also please give me 5 articles on the US Economy from the last week.  Also are hearing aids included in my Northwinds Standard Healthcare Plan? Also email bob@xxxxxxxx.com and tell him I am running late for lunch."**

ChatGPT determines it needs to perform the following external calls:

1) getCurrentUTCDateTime - system function to obtain the UTC date.
2) getDogName - system function to return a random dog name. :-)
3) getWeather - to obtain the weather in London (this is a free api you can sign up for at weatherapi.com)-
4) getNews - to obtain 4 news articles on the US Economy (this is a free api you can sign up for at newsapi.org)
5) getPineconeData - this illustrates how chatGPT can format a query to an external vector database and return silo'd information (you can sign up for a free Pinecone database at Pinecone.io).
6) sendEmail - this is fun - chatGPT can be a personal assistant for you, sending out emails.

The result is as follows (failed to give me sightseeing tips, but did give me 5 citations from external data sources, and send an email!):

```
  "message": {
        "role": "assistant",
        "content": "Your dog's name is Snoopy. 
        
        The current time in PST is 12:52 PM.
        
        The weather in London is partly cloudy with a temperature of 18.0\u00b0C (64.4\u00b0F).
        
        For sightseeing activities in London, I would recommend visiting popular attractions 
        such as the Tower of London, Buckingham Palace, the British Museum, the London Eye, 
        and taking a boat tour on the River Thames. Additionally, you can explore the vibrant 
        neighborhoods of Covent Garden, Camden Town, and Notting Hill. Don't forget to check 
        out the West End for world-class theater performances.
        
        Here are 5 articles on the US Economy from the last week:\
        
        1. Title: \"On-Orbit Satellite Servicing, New Crew Capsules and Artificial Gravity: 
        NASA's Latest Tech Initiative\"   
        Description: \"A new Blue Origin crewed spacecraft is in the works as part of a NASA collaboration 
        designed to advance the orbital economy, with the space agency lending its expertise to seven 
        different commercial partners.\"
        
        2. Title: \"Partial de-dollarization is possible, but China won't dethrone the greenback even if 
        it becomes the world's largest economy\"
        Description: \"History suggests that dollar dominance could carry on well into the second half 
        of the 21st century, even if China's economy outpaces the US.\"
        
        3. Title: \"Federal Reserve officials announce pause in US interest-rate hikes\"
        Description: \"Even with the pause, Fed officials suggest further increases may come depending on 
        how close the economy gets to the 2% inflation target. US Federal Reserve officials have announced 
        a pause in interest-rate hikes, leaving rates at 5% to 5.25% after more than a year of...\"
        
        4. Title: \"Forget de-dollarization - Argentina may adopt the greenback as its currency and abandon the peso\"   
        Description: \"If Argentina adopts the greenback, it would become the biggest economy so far to 
        dollarize, according to Bloomberg.\"
        
        5. Title: \"The US economy is entering expansion, not recession, and investors fear they are missing 
        out, Fundstrat's Tom Lee says\"
        Description: \"The US is entering a phase of economic expansion and not a recession, which means 
        the stock-market rally will become more broad-based, Fundstrat's Tom Lee has said.\"
        
        Regarding your question about hearing aids, according to the information I have, hearing aids are 
        included in the Northwinds Standard Healthcare Plan. The plan covers routine hearing aid maintenance, 
        repair, counseling, evaluations, and hearing aid accessories. However, services provided by 
        out-of-network providers may not be covered fully. It's always best to check with your healthcare 
        plan for details and specifics.
        
        I have sent an email to bob@xxxxxxxx.com informing him that you are running late for lunch."
      },
      "finish_reason": "stop"
    }
    
```

Here is the email chatGPT executed (this literally arrived in an inbox!):

```
From: <xxx@yyy.com>
Date: Sun, Jun 18, 2023 at 12:52 PM
Subject: Running late for lunch
To: <bob@xxxxxxxx.com>


Hi Bob, just wanted to let you know that I am running late for lunch. See you soon!
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
