from flask import Flask, request, jsonify, render_template
import nltk
from nltk.corpus import wordnet
from googletrans import Translator

# Download wordnet data (if you haven't already)
nltk.download('wordnet')

app = Flask(__name__)
translator = Translator()

def is_word_correct(word):
    return wordnet.synsets(word)

def get_corrections(word):
    from nltk.metrics.distance import edit_distance
    words = set(wordnet.words())
    corrections = [(w, edit_distance(word, w)) for w in words if w[0] == word[0]]
    corrections = sorted(corrections, key=lambda x: x[1])
    return [word for word, _ in corrections[:5]]

def translate_to_hindi(word):
    translation = translator.translate(word, src='en', dest='hi')
    return translation.text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_spelling():
    data = request.get_json()
    word = data.get("word", "").strip().lower()

    if is_word_correct(word):
        hindi_meaning = translate_to_hindi(word)  # Get Hindi meaning
        response = {"word": word, "correct": True, "suggestions": [], "hindi_meaning": hindi_meaning}
    else:
        suggestions = get_corrections(word)
        response = {"word": word, "correct": False, "suggestions": suggestions}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
