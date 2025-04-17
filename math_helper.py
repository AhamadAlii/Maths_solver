import whisper
import speech_recognition as sr
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
import pyttsx3
from sympy import symbols, Eq, solve

# Define variable for equations
x = symbols('x')

# Text-to-speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Preprocess natural language math expressions
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
    # handle 'x' as variable only when not used as a word
    text = text.replace(" x ", " x")  # fix spacing issue
    return text

# Solve math expressions
def solve_expression(expr):
    try:
        expr = preprocess_expression(expr)
        expr = expr.replace("^", "**")  # convert power operator
        if '=' in expr:
            left, right = expr.split('=')
            solution = solve(Eq(eval(left), eval(right)), x)
            return f"The solution is: {solution}"
        else:
            result = eval(expr)
            return f"The result is: {result}"
    except Exception as e:
        return f"❌ Could not solve the problem: {e}"

# Transcribe voice using Whisper
def whisper_transcribe(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result['text']

# Record from mic and save to WAV
def record_audio(filename="voice_input.wav"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("🎤 Speak your math problem...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
    return filename

# Extract math expression from image
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

# Main program
def main():
    print("🔢 Math Helper")
    print("Choose input method:\n[1] Voice (mic)\n[2] Image (file)")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        audio_file = record_audio()
        text = whisper_transcribe(audio_file)
        print(f"🗣 Recognized: {text}")
    elif choice == '2':
        image_path = input("Enter the path to the image file: ")
        text = extract_text_from_image(image_path)
        print(f"🖼 Extracted: {text}")
    else:
        print("❌ Invalid input.")
        return

    result = solve_expression(text)
    print(f"✅ {result}")
    speak(result)

if __name__ == "__main__":
    main()
