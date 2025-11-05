from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from pathlib import Path

project_root = Path(__file__).parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path)

MODEL = "gpt-3.5-turbo"

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))


# 1. Define a list of callable tools for the model
tools = [
      {
        "type": "function",
        "name": "click_button",
        "description": "Clicks a button in a gui with a certain color",
        "parameters": {
            "type": "object",
            "properties": {
                "button_color": {
                    "type": "string",
                    "description": "a color in swedish or english",
                },
            },
            "required": ["button_color"],
        },
    },
]
def click_button(button_color):
    print(f"Du tryckte på den {button_color} knappen!")

# Create a running input list we will add to over time
def query_ai(prompt):
    print("prompting ai with: " + prompt)
    input_list = [{"role": "user", "content": prompt}]

    # 2. Prompt the model with tools defined
    response = client.responses.create(
        model=MODEL,
        tools=tools,
        input=input_list,
    )

    for item in response.output:
        if item.type == "function_call":
            if item.name == "click_button":
                args = json.loads(item.arguments)
                click_button(args["button_color"])


   # print("Tool Calling response:")
   # print(response.model_dump_json(indent=2))

#response = client.responses.create(
#    model=MODEL,
#    instructions="Use the tools when the user wants to do something, requests could be in swedish or english",
#    tools=tools,
#    input=input_list,
#)
#print("Response for user:")
#print(response.model_dump_json(indent=2))
#print("\n" + response.output_text)
