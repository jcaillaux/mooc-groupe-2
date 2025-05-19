from langdetect import detect
from pymongo import MongoClient
import pandas as pd

from transformers import pipeline

# Load the classification pipeline with the specified model
# pipe = pipeline("text-classification",
#                model="tabularisai/multilingual-sentiment-analysis")
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_map = {0: "Very Negative", 1: "Negative",
                 2: "Neutral", 3: "Positive", 4: "Very Positive"}


def predict_sentiment(texts):
    inputs = tokenizer(texts, return_tensors="pt",
                       truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    sentiment_map = {0: "Very Negative", 1: "Negative",
                     2: "Neutral", 3: "Positive", 4: "Very Positive"}
    return [{'sentiment': sentiment_map[p], 'score': probabilities.tolist()[0]} for p in torch.argmax(probabilities, dim=-1).tolist()]


def detect_sentiment(text: str):
    # global pipe

    # return pipe(text)
    return predict_sentiment(text)


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
