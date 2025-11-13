from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from pathlib import Path

from tool_calling.ai_tools import get_tools

from event_loop_runner import run_async, send_event

project_root = Path(__file__).parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path)

MODEL = "gpt-3.5-turbo"

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))



async def write_question(question):
    await send_event("runFunction", {"name": "write_question", "args": question})

async def send_question():
     await send_event("runFunction", {"name": "send_question"})

async def change_backend(backend):
    await send_event("runFunction", {"name": "change_backend", "args": backend})


def query_ai(prompt):
    print("prompting ai with: " + prompt)
    input_list = [{"role": "user", "content": prompt}]
    tools = get_tools()

    response = client.responses.create(
        model=MODEL,
        tools=tools,
        input=input_list,
    )

    for item in response.output:
        if item.type == "function_call":
            print("AI is using function:", item.name, "with arguments", item.arguments)

            args = json.loads(item.arguments)
            print("args:", args) 

            if item.name == "write_question":
                question_text = args.get("question")
                run_async(write_question(question_text))
            elif item.name == "send_question":
                run_async(send_question())
            elif item.name == "change_backend":
                backend = args.get("backend")
                run_async(change_backend(backend))

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
 

