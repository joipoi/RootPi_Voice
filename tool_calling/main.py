from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from pathlib import Path

from tools import get_tools

project_root = Path(__file__).parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path)

MODEL = "gpt-3.5-turbo"

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))



def write_question(question):
    print(f"")

def post_question():
    print(f"")

def change_backend(backend):
    print(f"")




# Create a running input list we will add to over time
def query_ai(prompt):
    print("prompting ai with: " + prompt)
    input_list = [{"role": "user", "content": prompt}]
    tools = get_tools()

    # 2. Prompt the model with tools defined
    response = client.responses.create(
        model=MODEL,
        tools=tools,
        input=input_list,
    )

    for item in response.output:
        if item.type == "function_call":
            print("AI is using function: " + item.name + " with arguments " + item.arguments)
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
