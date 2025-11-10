

def get_tools():
    # 1. Define a list of callable tools for the model
    question_tool =  {
            "type": "function",
            "name": "write_question",
            "description": "skriver en fråga ställd av användaren till en chatbot som är expert på bekämpningsmedel",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "frågan som användaren vill fråga",
                    },
                },
                "required": ["question"],
            },
        },
    
    post_tool =  {
            "type": "function",
            "name": "post_question",
            "description": "Trycker på en knapp som skickar en fråga från användaren till en ai chatbot"
        },
    
    change_backend_tool =  {
            "type": "function",
            "name": "change_backend",
            "description": "väljer ett alternativ i en droppdown dom ändrar vilken backend vi använder, alternativ är RAG eller Live",
             "parameters": {
                "type": "object",
                "properties": {
                    "backend": {
                        "type": "string",
                        "description": "Vilken backend som ska väljas, måste vara RAG eller Live",
                    },
                },
                "required": ["backend"],
            },
        },

    tools = [question_tool, post_tool, change_backend_tool]
    return tools