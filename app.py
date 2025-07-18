
from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image
from moviepy.editor import VideoFileClip
from fpdf import FPDF

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert_file():
    uploaded_file = request.files["file"]
    output_format = request.form["output_format"]
    filename = secure_filename(uploaded_file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    uploaded_file.save(file_path)

    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    try:
        if ext == ".txt" and output_format == "pdf":
            pdf_path = os.path.join(UPLOAD_FOLDER, f"{name}.pdf")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    pdf.cell(200, 10, txt=line.strip(), ln=True)
            pdf.output(pdf_path)
            return send_file(pdf_path, as_attachment=True)

        elif ext == ".png" and output_format == "jpg":
            img = Image.open(file_path).convert("RGB")
            output_path = os.path.join(UPLOAD_FOLDER, f"{name}.jpg")
            img.save(output_path, "JPEG")
            return send_file(output_path, as_attachment=True)

        elif ext == ".mp4" and output_format == "mp3":
            output_path = os.path.join(UPLOAD_FOLDER, f"{name}.mp3")
            clip = VideoFileClip(file_path)
            clip.audio.write_audiofile(output_path)
            return send_file(output_path, as_attachment=True)

        elif ext == ".jpg" and output_format == "webp":
            img = Image.open(file_path).convert("RGB")
            output_path = os.path.join(UPLOAD_FOLDER, f"{name}.webp")
            img.save(output_path, "WEBP")
            return send_file(output_path, as_attachment=True)

        else:
            return "Conversion not supported for selected file type and output format."

    except Exception as e:
        return f"Error during conversion: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
