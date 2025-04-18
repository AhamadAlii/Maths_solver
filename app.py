import os
from flask import Flask, render_template, request
from solver import solve_expression, extract_text_from_image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if 'math_text' in request.form and request.form['math_text'].strip():
            text = request.form['math_text']
            result = solve_expression(text)
        elif 'image_file' in request.files:
            image = request.files['image_file']
            if image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                extracted_text = extract_text_from_image(image_path)
                result = solve_expression(extracted_text)
    return render_template('index.html', result=result)
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

