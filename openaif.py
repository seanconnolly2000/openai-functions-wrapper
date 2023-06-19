import openai
import json
from typing import List
from functions.chat import functions

# openai with functions - openaif
# The secret to using functions is to establish a dialog that chatcompletion can refer back to.
# This is done by storing all messages from the user, from the function, and from the assistant (chat) in messages and passing them!


class openaif:
    # To initialize, you'll need to pass your API key and list of functions.  You can change your model if you are using gpt4
    def __init__(self, api_key: str, functions: functions):
        self.api_key = api_key
        self.openai = openai
        self.model = "gpt-3.5-turbo-16k-0613"  # gpt-4-0613 , gpt-3.5-turbo-16k-0613 , gpt-3.5-turbo-0613
        self.openai.api_key = self.api_key
        self.openai.Engine.list()["data"][0]  # will throw an error if invalid key
        self.temperature = 0  # note: people have noticed chatGPT not including required parameters.  Setting temperature to 0 seems to fix that
        self.messages = []
        self.maximum_function_content_char_size = 8000  # to prevent token overflow
        self.functions = functions
        self.infinite_loop_counter = (
            0  # don't want to burn through too many openai credits :-)
        )

    # This is a preamble adhered to throughout the session since it uses the "system" role:  "Act like you are a..."
    # Feel free to experiment with the system role.  In my experiments, this seems to cause problematic output including sending content through in the same responses that also request a function_call.
    def set_chat_context(self, prompt: str):
        self.messages.insert(0, {"role": "system", "content": prompt})

    def clear_chat_session(self):
        self.messages = []

    def user_request(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})
        res = self.call_openai()
        if res["choices"][0]["message"]:
            self.messages.append(res["choices"][0]["message"])
            while res["choices"][0]["finish_reason"] == "function_call":
                self.infinite_loop_counter += 1
                if self.infinite_loop_counter > 100:
                    exit()  # you can do whatever you want, but if chatgpt is instructing continuous function calls, something needs to be looked at
                function_name = res["choices"][0]["message"]["function_call"]["name"]
                function_args = json.loads(
                    res["choices"][0]["message"]["function_call"]["arguments"]
                )
                # As mentioned, security is always a concern when allowing a 3rd party system to execute functions on your servers!!!
                # This call assures that you've at least passed these functions to chatGPT.
                # You should also consider scrubbing the parameters to prevent SQL or other injections!
                if function_name in self.functions:
                    modules = __import__("functions.samples")
                    funct = getattr(modules, function_name)
                    function_response = str(
                        funct(**function_args)
                    )  # responses must be string in order to append to messages
                    if len(function_response) > self.maximum_function_content_char_size:
                        function_response = function_response[
                            : self.maximum_function_content_char_size
                        ]
                    res = self.function_call(function_name, function_response)
        return res

    def function_call(self, function: str, function_response: str):
        self.messages.append(
            {"role": "function", "name": function, "content": function_response}
        )
        res = self.call_openai()
        if res["choices"][0]["message"]:
            self.messages.append(res["choices"][0]["message"])
        return res

    def call_openai(self) -> str:
        # function_object = json.loads(str(functions))
        if self.functions == []:
            res = self.openai.ChatCompletion.create(
                model=self.model,
                temperature=self.temperature,
                messages=self.messages,
            )
        else:
            res = self.openai.ChatCompletion.create(
                model=self.model,
                temperature=self.temperature,
                messages=self.messages,
                functions=self.functions.to_json(),
            )
        # uncomment if you want to see the communications:
        print(self.functions.to_json())
        print(self.messages)
        print(res)
        return res
