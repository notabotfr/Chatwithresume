from flask import Flask, request, render_template
import os
from model import predict_category

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Homepage
@app.route("/")
def home():
    return render_template("home.html")

# Handle File Upload
@app.route("/predict", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    predicted_category = predict_category(file_path)
    
    return render_template("result.html", category=predicted_category)

# Serve Upload Form
@app.route("/upload", methods=["GET"])
def upload_form():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
