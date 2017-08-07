from flask import Flask
from flask_ask import Ask, question, statement
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize

app = Flask(__name__)
ask = Ask(app, "/")

#Import the data from a csv file

csvdata = pd.read_csv('training_data.csv', skipinitialspace=True,delimiter=",")

#Convert data into a numpy array
csvdata1 = np.array(csvdata)
train = []

#Put contents of numpy array into empty list
train.extend(csvdata1)

nltk.download('punkt')

#Process the user input by tokenizing it
@ask.launch
def startSkill():
    msg = "Hello, welcome to the There-A.I.-pest. Can I help you?"
    return question(msg)

@ask.intent("YesIntent")
def theraipy():
    msg = "What seems to be the problem?"
    return question(msg)

@ask.intent("NoIntent")
def happy():
    msg = "Okay. If you need anything, I'll be waiting!"
    return statement(msg)

@ask.intent("AdviceIntent")
def give_advice():
    msg = "What do you need help with?"
    return question(msg)

@ask.intent("TherapyIntent")
def theraipy(line):
    try:

        wordlist = set(word.lower() for statement in train for word in word_tokenize(statement[0]))

        x = [({word: (word in word_tokenize(x[0])) for word in wordlist}, x[1]) for x in train]

        classifier = nltk.NaiveBayesClassifier.train(x)

        test_data = line
        if line.__len__() > 1:

            # If there is a string, return if string is labeled as positive or negative
            test_data_features = {word.lower(): (word in word_tokenize(test_data.lower())) for word in wordlist}
            sentiment = (classifier.classify(test_data_features))
        else:
            msg = "I'm sorry, can you repeat that?"
            return question(msg)
        if sentiment == "pos":
            line.replace("am", "are")
            line.replace("I","you")
            line.replace("I'm","you're")
            msg = "I am glad that "+line+" . Would you like to tell me more?"
            return question(msg)

        if sentiment == "neg":
            if "kill myself" in line:
                msg = "It appears that you are feeling suicidal. Please, tell me more. Why are you feeling this way?"
                return question(msg)
            else:
                msg = "I'm sorry that you're feeling sad. Can you elaborate?"
                return question(msg)


    except Exception, e: return str(e)

if __name__ == '__main__':
    app.run(debug=True)

