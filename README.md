##Resume Classification & Retrieval-Augmented Generation (RAG) System

This project consists of two Flask-based applications:
Resume Classification System - A web app that classifies resumes into predefined categories.
Retrieval-Augmented Generation (RAG) System - A chatbot-powered document retrieval system using FAISS and LangChain.

##Features

##Resume Classification System
Upload a resume (PDF, DOCX, or TXT)
Extracts text from the uploaded document
Uses a trained machine learning model (KNN) to predict the resume category
Displays the predicted category on a result page

##RAG System
Uploads and processes documents (PDF, DOCX, TXT, Markdown)
Creates a vector store using FAISS
Retrieves context relevant to user queries
Generates responses using an LLM (Ollama)

##Steps to run it 
Clone repo, check paths
Install ollama from ollama.com
After successfull installation, type this in your CMD: ollama run <modelname> (remember to specify the model name in the chatbot.js file!)
check if ollama is running sucessfully by pasting this in your browser http://localhost:11434/api/generate

Run the application by typing python app.py in your terminal
