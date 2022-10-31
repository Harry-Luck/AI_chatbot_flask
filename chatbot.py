from asyncio.windows_events import NULL
import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

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

bot_name = "Sam"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
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
                return random.choice(intent['responses'])
    
    return "I do not understand..."

def chatbot_respond(user_query,lang = "en"):
    if user_query == "Hi":
        return ["Nice to meet you like this. What can I do for you?", NULL]
    
    if user_query == "hi":
        return ["Nice to meet you like this. What can I do for you?", NULL]
    
    if user_query == "How to build business plan?":
        return ["I'm not sure I understand 100% what do you mean but here is what I suggest for you.", "How to use the business blan builder?;How to download business plan?;Business plan best practices?"] 

    if user_query == "How to use the business blan builder?":
        return ["We offer the creation of a Business Plan to customers, often startups, to define the company’s economic and financial analysis model, objectives, balance sheet analysis and related risks.", NULL] 

    if user_query == "How to download business plan?":
        return ["Download this simple business plan template in MS Word, PDF or Google Doc format and write your professional business plan in no time.", NULL] 

    if user_query == "Business plan best practices?":
        return ["Create your Tech Startup and become a Tech Entrepreneur.", NULL] 

    if user_query == "Build an initial business plan":
        return ["The following videos can help you.", NULL]
    

    return ["I have found some vides that might be helpful to you, you watch them instantly by clicking on the video icon.", NULL]

def find_pdfResource(msg):
    
    return "I do not understand..."

def video_search(user_query,lang = "en"):
    if user_query == "Build an initial business plan": 
        return "./static/images/video1.mp4;./static/images/video2.mp4;./static/images/video3.mp4"

    return ""


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

