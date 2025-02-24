from flask import Flask, render_template, request, jsonify
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

app = Flask(__name__)

class SimpleRAG:
    def __init__(self, model_name="qwen2.5", embedding_model="all-MiniLM-L6-v2"):
        self.llm = Ollama(model=model_name)
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.vectorstore = None

    def load_document(self, file_path):
        file_extension = os.path.splitext(file_path)[1].lower()
        try:
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension in ['.docx', '.doc']:
                loader = UnstructuredWordDocumentLoader(file_path)
            elif file_extension in ['.txt', '.md']:
                loader = TextLoader(file_path, encoding='utf-8')
            else:
                return f"❌ Unsupported file type: {file_extension}"
            
            return loader.load()
        except Exception as e:
            return f"❌ Document Loading Error: {e}"

    def process_documents(self, file_path, chunk_size=500, chunk_overlap=50):
        documents = self.load_document(file_path)
        if isinstance(documents, str):
            return documents

        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            texts = text_splitter.split_documents(documents)
            self.vectorstore = FAISS.from_documents(texts, self.embeddings)
            return f"✅ Created vector store with {len(texts)} document chunks"
        except Exception as e:
            return f"❌ Document Processing Error: {e}"

    def retrieve_context(self, query, top_k=3):
        if not self.vectorstore:
            return "🚫 No document loaded."
        
        try:
            results = self.vectorstore.similarity_search(query, k=top_k)
            return "\n\n".join([doc.page_content for doc in results])
        except Exception as e:
            return f"❌ Context Retrieval Error: {e}"

    def generate_response(self, query):
        context = self.retrieve_context(query)
        augmented_query = f"""
        Context from document:
        {context}

        User Query: {query}

        Provide a precise answer based on the document context.
        If no relevant information is found, clearly state that.
        Always be objective.
        """
        return self.llm.invoke(augmented_query)

rag = SimpleRAG()

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    process_result = rag.process_documents(file_path)
    return jsonify({'message': process_result})

@app.route('/query', methods=['POST'])
def query_rag():
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'})
    
    response = rag.generate_response(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
