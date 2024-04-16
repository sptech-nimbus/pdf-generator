import io
from reportlab.pdfgen import canvas
from flask import Flask, request, make_response
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

app = Flask(__name__)

@app.route("/pdf-gen", methods=["POST"])
def post_pdf_gen():
    data = request.get_json()

    pdf = pdf_generation(data)

    with open(f"Ficha-técnica-{data['name']}.pdf", "wb") as f:
        f.write(pdf)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"

    return response

def pdf_generation(data):
    pdfmetrics.registerFont(TTFont('Catamaran-Bold', './fonts/Catamaran-Bold.ttf'))

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    title = title_gen(c, "Ficha de jogador")
    
    image = athlete_image_gen(c, data['athlete-image'], title)

    athlete_name_gen(c, data['name'], image)
    
    # image = ImageReader('url')
    
    c.save()

    buffer.seek(0)

    return buffer.read()

def title_gen(c, text):
    title = c.beginText()
    
    _fontSize = 24
    _fontName = "Catamaran-Bold"
    
    text_width = c.stringWidth(text, fontSize = _fontSize, fontName = _fontName)
    
    title.setTextOrigin((A4[0] - text_width) / 2, A4[1] - 40)
    title.setFont(_fontName, _fontSize)
    title.textLine(text)
    
    c.drawText(title)
    
    return title

def athlete_image_gen(c, url, title):
    image = ImageReader(url)
    image_width = 175
    image_heigth = 240
    
    c.drawImage(image, 40, (title.getY() - image_heigth), width = image_width, height = image_heigth)
    
    return image

def athlete_name_gen(c, name, image):
    name_text = c.beginText()
    
    print(image.getSize()[0])
    
    name_text.setTextOrigin(40, image.getSize()[0])
    name_text.textLine(name)
    
    c.drawText(name_text)
    
    return name_text