# Resume Classification & Retrieval-Augmented Generation (RAG) System

<p align="center">
  This project consists of two Flask-based applications: Resume Classification System and Retrieval-Augmented Generation (RAG) System.
</p>

## **Features**

### **Resume Classification System**
- **Upload a resume** (PDF, DOCX, or TXT)
- **Extracts text** from the uploaded document
- **Uses a trained machine learning model (KNN)** to predict the resume category
- **Displays the predicted category** on a result page

### **RAG System**
- **Uploads and processes documents** (PDF, DOCX, TXT, Markdown)
- **Creates a vector store** using FASS
- **Retrieves context** relevant to user queries
- **Generates responses** using an LLM (Ollama)

## **Steps to Run It**

1. **Clone the repository** and check paths.
2. **Install Ollama** from [ollama.com](https://ollama.com).
3. **Check status** paste http://localhost:11434/api/generate in your browser to check if ollama is running.
4. After successful installation, type this in your CMD:
   ```bash
   ollama run <model_name>
  <p align="center"> Make sure to change your model name in the chatbot.js file! (I have used qwen2.5) </p> ```

