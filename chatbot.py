import random
import json
import pickle
import numpy as np
import nltk
from pymongo import MongoClient
from datetime import datetime

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

lemmatizer = WordNetLemmatizer()

# Conectar a MongoDB
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['chatbot_db']
    collection = db['user_queries']
    print("Conexión a la base de datos exitosa")
except Exception as e:
    print(f"Ocurrió un error al conectar a la base de datos: {e}")

# Abrir el archivo en modo lectura
intents = json.loads(open('intents_spanish.json', 'r', encoding='utf-8').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.20
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    if not intents_list:
        return "Lo siento, no tengo la capacidad para responderte esto."
    
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    
    return "Lo siento, no tengo la capacidad para responderte esto."

def save_user_query(query, response):
    document = {
        "query": query,
        "response": response,
        "timestamp": datetime.now()
    }
    collection.insert_one(document)




