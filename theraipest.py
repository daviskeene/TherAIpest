from flask import Flask
from flask_ask import Ask, question, statement
import nltk
from nltk.tokenize import word_tokenize

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def startSkill():
    msg = "Hello, welcome to the Ther-AI-pest. Would you like to have a chat?"
    return question(msg)

@ask.intent("YesIntent")
def theraipy():

    train = [("Great place to be when you are in Bangalore.", "pos"),
             ("The place was being renovated when I visited so the seating was limited.", "neg"),
             ("Loved the ambience, loved the food", "pos"),
             ("The food is delicious but not over the top.", "neg"),
             ("Service - Little slow, probably because too many people.", "neg"),
             ("The place is not easy to locate", "neg"),
             ("Mushroom fried rice was spicy", "pos"),
             ("I hated the food. It was terrible", "neg"),
             ("The food did not satisfy me.", "neg")
             ]

    dictionary = set(word.lower() for passage in train for word in word_tokenize(passage[0]))

    t = [({word: (word in word_tokenize(x[0])) for word in dictionary}, x[1]) for x in train]

    classifier = nltk.NaiveBayesClassifier.train(t)

    test_data = "The food was poisoned by the chinese. I absolutely hated it."
    test_data_features = {word.lower(): (word in word_tokenize(test_data.lower())) for word in dictionary}

    print (classifier.classify(test_data_features))

if __name__ == '__main__':
    app.run(debug=True)

