import PyPDF2
import docx
import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier

# Function to extract text from files
def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF, DOCX, or TXT file.")

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + " "
    return text.strip()

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()

# Load dataset and train model
def train_model():
    resumeDataSet = pd.read_csv("UpdatedResumeDataSet.csv")  # Make sure the dataset is in the same folder
    requiredText = resumeDataSet['Resume']
    requiredTarget = resumeDataSet['Category']

    word_vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words='english')
    word_vectorizer.fit(requiredText)
    WordFeatures = word_vectorizer.transform(requiredText)

    X_train, X_test, y_train, y_test = train_test_split(WordFeatures, requiredTarget, test_size=0.2, stratify=requiredTarget, random_state=42)

    clf = OneVsRestClassifier(KNeighborsClassifier())
    clf.fit(X_train, y_train)

    return clf, word_vectorizer

model, vectorizer = train_model()

# Function to predict category
def predict_category(file_path):
    resume_text = extract_text_from_file(file_path)
    input_features = vectorizer.transform([resume_text])
    predicted_category = model.predict(input_features)[0]
    return predicted_category
