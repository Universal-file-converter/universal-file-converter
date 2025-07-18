
from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)
            output_path = os.path.join(CONVERTED_FOLDER, file.filename)
            with open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
                f_out.write(f_in.read())  # Fake conversion for demo
            return send_file(output_path, as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

