from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["file"]
    conversion_type = request.form["conversion"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    name, ext = os.path.splitext(filename)
    output_path = os.path.join(CONVERTED_FOLDER, f"{name}_converted")

    # Handle basic image conversions
    if conversion_type == "jpg2png" and ext.lower() in [".jpg", ".jpeg"]:
        output_path += ".png"
        Image.open(filepath).save(output_path, "PNG")
    elif conversion_type == "png2jpg" and ext.lower() == ".png":
        output_path += ".jpg"
        Image.open(filepath).convert("RGB").save(output_path, "JPEG")
    # Handle txt <-> pdf/doc dummy conversion (just rename)
    elif conversion_type == "txt2pdf" and ext.lower() == ".txt":
        output_path += ".pdf"
        os.rename(filepath, output_path)
    elif conversion_type == "pdf2txt" and ext.lower() == ".pdf":
        output_path += ".txt"
        os.rename(filepath, output_path)
    else:
        return "Unsupported file type or conversion"

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
    
