import json
import os
import argparse
import sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("API key not found!!")

#Import the OpenAI class from the openai library and create a client. 
#The key trick is that we point the client's base_url at OpenRouter instead of OpenAI's default
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

#argparse object to get the user prompt from the command line
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

#get response from the model
for _ in range(20):  # Retry up to 20 times
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)

            if not result_message["content"]:
                raise Exception("Tool call returned an empty result")

            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(f"Final response:\n{message.content}")
        break

#if 20 iterations complete and no response is generated, exit with an error
else:   
    print("Error: Maximum agent iterations reached.")
    sys.exit(1)

# Print token usage if verbose mode is enabled
if response.usage is None:
    raise RuntimeError("Response usage is None!!")
else:   
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")




