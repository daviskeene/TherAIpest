from flask import Flask
from flask_ask import Ask, question, statement
import theraipy
import nltk
from nltk.tokenize import word_tokenize

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def startSkill():
    msg = "Hello, welcome to the Ther-AI-pest. Can I help you?"
    return question(msg)

@ask.intent("YesIntent")
def theraipy():
    msg = "What seems to be the problem?"
    return question(msg)

@ask.intent("NoIntent")
def happy():
    msg = "I'm glad that you are feeling happy. What was the best part of your day?"
    return question(msg)

@ask.intent("ElaborateIntent")
def elab(extension):
    try:
        process = theraipy.elaborate(extension)
        return process

    except:
        msg = "Sorry, I must have misunderstood you. Can you repeat that?"
        return question(msg)

@ask.intent("TherapyIntent")
def theraipy(line):
    try:
        sentiment = theraipy.process(line)

        if sentiment == "pos":
            msg = "I am glad that you are feeling well. Would you like to continue to speak?"
            return question(msg)
        if sentiment == "neg":
            if "kill myself" in line:
                msg = "I am sorry that you are feeling suicidal."
                return statement(msg)

    except:
        msg = "Sorry, I must have misunderstood you. Can you try again?"
        return question(msg)

if __name__ == '__main__':
    app.run(debug=True)

