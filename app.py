import os
from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
from sympy import symbols, Eq, solve, simplify, pretty
from PIL import Image
import pytesseract
import os

x = symbols('x')
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

def preprocess_expression(text):
    text = text.lower()
    text = text.replace("plus", "+").replace("minus", "-")
    text = text.replace("times", "*").replace("multiplied by", "*")
    text = text.replace("divided by", "/").replace("over", "/")
    text = text.replace("equals", "=").replace("equal to", "=")
    text = text.replace("power", "^")
    return text

def solve_expression(expr):
    try:
        original = expr.strip()
        cleaned = preprocess_expression(original)
        cleaned = cleaned.replace("^", "**")

        if '=' in cleaned:
            left, right = cleaned.split('=')
            result = solve(Eq(eval(left), eval(right)), x)
        else:
            result = eval(cleaned)

        steps = {
            "original": original,
            "cleaned": cleaned,
            "result": result
        }

        return f"The result is: {result}", steps

    except Exception as e:
        return f"❌ Could not solve the problem: {e}", None

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    steps = []

    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        if 'math_text' in request.form and request.form['math_text'].strip():
            text = request.form['math_text']
            result, steps = solve_expression(text)
            session['history'].append({'query': text, 'result': result, 'steps': steps})

        elif 'image_file' in request.files:
            image = request.files['image_file']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                image.save(image_path)
                extracted_text = extract_text_from_image(image_path)
                result = solve_expression(extracted_text)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
