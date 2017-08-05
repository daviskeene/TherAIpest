from flask import Flask
from flask_ask import Ask, question, statement
import theraipy
import nltk
from nltk.tokenize import word_tokenize

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def startSkill():
    msg = "Hello, welcome to the Ther-AI-pest. Are you feeling sad?"
    return question(msg)

@ask.intent("YesIntent")
def theraipy():
    msg = "What seems to be the problem?"
    return question(msg)

@ask.intent("NoIntent")
def happy():
    msg = "I'm glad that you are feeling happy. What was the best part of your day?"
    return question(msg)

@ask.intent("TherapyIntent")
def theraipy(line):
    sentiment = theraipy.process(line)

    if sentiment == "pos":
        msg = "I am glad that you are feeling well. Would you like to continue to speak?"
        return question(msg)
    if sentiment == "neg":
        if "kill myself" in line:
            msg = "I am sorry that you are feeling suicidal."
            return statement(msg)
if __name__ == '__main__':
    app.run(debug=True)

