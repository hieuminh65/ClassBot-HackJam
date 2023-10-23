import docx
import re
import PyPDF2
######################################
def read_docx(file_path):
    docx_file = file_path

    # Open the DOCX file
    doc = docx.Document(docx_file)

    # Loop through paragraphs in the document and print the text
    return doc.paragraphs



def read_pdf(pdf_file: str) -> [str]:
    # Open the PDF file of your choice
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
        for character in pdf_text:
            character.replace("\n", "")
            return pdf_text

##########################################################
def read_txt(file_path):
    # Open the text file for reading
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the contents of the file
        file_contents = file.read()
    # Print the file contents
    return file_contents


#read_pdf('TEALSReferenceGuide2022.pdf')
