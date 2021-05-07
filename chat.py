import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

from flask import Flask, render_template, request

app = Flask(__name__)

bot_response = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userInput = request.args.get('msg')
    userText = tokenize(userInput)
    X = bag_of_words(userText, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                # print(f"{bot_name}: {random.choice(intent['responses'])}")
                bot_response = random.choice(intent['responses'])


    else:
        # print(f"{bot_name}: I do not understand...")
        bot_response = "I do not understand"
    return bot_response


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

if __name__ == "__main__":
    app.run()



