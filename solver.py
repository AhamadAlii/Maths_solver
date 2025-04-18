from sympy import symbols, Eq, solve
from PIL import Image
import pytesseract

x = symbols('x')
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust if needed

def preprocess_expression(text):
    text = text.lower()
    text = text.replace("plus", "+")
    text = text.replace("minus", "-")
    text = text.replace("times", "*")
    text = text.replace("multiplied by", "*")
    text = text.replace("divided by", "/")
    text = text.replace("over", "/")
    text = text.replace("equals", "=")
    text = text.replace("equal to", "=")
    text = text.replace("power", "^")
    return text

def solve_expression(expr):
    try:
        expr = preprocess_expression(expr)
        expr = expr.replace("^", "**")
        if '=' in expr:
            left, right = expr.split('=')
            solution = solve(Eq(eval(left), eval(right)), x)
            return f"The solution is: {solution}"
        else:
            result = eval(expr)
            return f"The result is: {result}"
    except Exception as e:
        return f"❌ Could not solve the problem: {e}"

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)
