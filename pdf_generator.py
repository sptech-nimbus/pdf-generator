import io
from reportlab.pdfgen import canvas
from flask import Flask, request, make_response
from reportlab.lib.utils import ImageReader

app = Flask(__name__)

@app.route("/pdf-gen", methods=["POST"])
def hello_world():
    data = request.get_json()
    
    pdf = pdf_generation(data)
    
    with open(f"Ficha-técnica-{data['name']}.pdf", "wb") as f:
        f.write(pdf)
    
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    
    return response

def pdf_generation(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    
    c.setPageSize((595, 842))
    
    c.drawImage(ImageReader(data['athlete-image']), 10, 10)
    
    c.save()
    
    buffer.seek(0)
    
    return buffer.read()