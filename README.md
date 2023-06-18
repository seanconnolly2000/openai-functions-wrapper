# openai-functions-wrapper

I hope this helps demystify the pipeline for executing multiple requests with OpenAI's chatcompletion.

I've created function wrappers that allow you to create the format necessary for chatcompletion to request function execution and parameters.

I've also illustrated how you need to append your conversation to "messages" to make the chat pipeline and function information work correctly.

Hope this helps you!

In the example, I show how you can have chatGPT request data from multiple sources.  Based upon the following prompt:

**"What is my dog's name, tell me what time is it in PST, what is the weather like in London, and what sightseeing activities would you recommend for London this time of year?  Also please give me 5 articles on the US Economy from the last week.  Also are hearing aids included in my Northwinds Standard Healthcare Plan?"**

ChatGPT determines it needs to perform the following external calls:

1) getCurrentUTCDateTime - system function to obtain the UTC date.
2) getDogName - system function to return a random dog name. :-)
3) getWeather - to obtain the weather in London (this is a free api you can sign up for at weatherapi.com)-
5) getNews - to obtain 4 news articles on the US Economy (this is a free api you can sign up for at newsapi.org)
6) getPineconeData - this illustrates how chatGPT can format a query to an external vector database and return silo'd information (you can sign up for a free Pinecone database at Pinecone.io).

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
