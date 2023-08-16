import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
count = 0
name = ""

@app.route("/", methods=("GET", "POST"))
def index():
    global count
    global name
    #print(count)
    if count == 0:
        count += 1
        result = request.args.get("result")
        #print(count)
        return render_template("index.html", result="Enter Your name.")
    elif count == 1 and request.method =="POST":
        count += 1
        name = request.form["animal"]
        #print(count)
        response = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
            model = 'gpt-3.5-turbo',
            messages = [ # Change the prompt parameter to the messages parameter
            {'role': 'user', 'content': f"In a short paragraph describe a small bedroom with a door and a bed. mention that the door is locked. mention that above the door is a sign that says Welcome {name}. do not add more than this. Begin and end the paragraph with the symbol $. do not include html type script in content."}
            ],
            temperature = 0
        )

        temp = f"{response.choices[0]}"
        beginning = temp.find("$") + 1
        temp = temp[beginning:]
        end = temp.find("$")
        temp = temp[:end] + " Look for the key."

        return redirect(url_for("index", result=temp))
        keyFound = False
        input = request.form["animal"]
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [{
                'role': 'user', 'content': f"{input}. If the first sentence mentions looking under the bed then say the key has been found and describe a key, oterwise say the key is not there. include $ at the beginning of they find the key."
            }],
            temperature = 0
        )
        temp = f"{response.choices[0]}"
        
        return redirect(url_for("index", result=response.choices[0]))
    
    elif request.method == "POST":
        animal = request.form["animal"]
        response = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
            model = 'gpt-3.5-turbo',
            messages = [ # Change the prompt parameter to the messages parameter
            {'role': 'user', 'content': generate_prompt(animal)}
            ],
            temperature = 0  
)
        print(response)
        return redirect(url_for("index", result=response.choices[0]))
    
    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """generate the beginning of a text adventure game about {}
    
    """.format(animal.capitalize())

def beginning_prompt():
    response = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
            model = 'gpt-3.5-turbo',
            messages = [ # Change the prompt parameter to the messages parameter
            {'role': 'user', 'content': "Describe a room. This room must include a door, a bed, and under that bed is a key, but do not mention the key" }
            ],
            temperature = 0
    )
    result = request.args.get("result")
    return render_template("index.html", result=result)

