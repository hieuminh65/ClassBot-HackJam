
from config import Config
from PyPDF2 import PdfFileReader
from flask import Flask, request, render_template
from PyPDF2 import PdfFileReader
import docx
import re
import PyPDF2
from read import read_pdf,read_docx,read_txt

# from read import read_docx,read_pdf,read_txt
app = Flask(__name__)
app.config.from_object(Config)
app=Flask(__name__,template_folder='templates')
import os


#list of file allowed
ALLOWED_EXTENSIONS = {'txt','docx','pdf','mp3','mp4','wav'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/", methods=["GET", "POST"])
def upload_file():
    print("running")
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file and allowed_file(uploaded_file.filename):
            # Save the uploaded file to a specific location or process it as needed
            # For example, you can save it to the current directory:
            file_path = uploaded_file.filename
            uploaded_file.save(file_path)
            #for pdf file
            pdf_text=read_pdf(file_path)
            for text in pdf_text:
                print(text)
            #for txt file
            print(read_txt(file_path))
            #for docx file
            docx_text=read_docx(file_path)
            for text in docx_text:
                print(text)
            return f"File '{uploaded_file.filename}' uploaded successfully."
        else:
            return f"File '{uploaded_file.filename}' can not be uploaded.\nPlease try again."
        

    return render_template("upload.html")
    



def main():
    print('working')
   
if __name__ == "__main__":
    print("Hello I'm Working")
    app.run(host="0.0.0.0", port=8000, debug=True)
    main()

