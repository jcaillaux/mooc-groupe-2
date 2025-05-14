from langdetect import detect
from pymongo import MongoClient
import pandas as pd

from transformers import pipeline

# Load the classification pipeline with the specified model
pipe = pipeline("text-classification",
                model="tabularisai/multilingual-sentiment-analysis")


def detect_sentiment(text: str):
    global pipe
    return pipe(text)


def detect_lang(text: str):
    return detect(text)


client = MongoClient('mongodb://localhost:27017/')
filter = {}
project = {
    'body': 1
}

results = client['mooc']['documents'].find(
    filter=filter,
    projection=project
)

for result in results:
    msg = result['body']
    print(detect_lang(msg), detect_sentiment(msg))
