# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, jsonify, Response
from dictionnary import Dictionnary

MAX_AUTOCOMPLETE_RESULTS = 15

app = Flask(__name__)

dictionnary = Dictionnary()
dictionnary.load(url="https://raw.githubusercontent.com/dwyl/english-words/master/words.txt")

@app.route('/', methods=['GET'])
def user_help():
    return "Give a word to test in the URL"

@app.route('/autocomplete/<string:start_with>', methods=['GET'])
def autocomplete(start_with):
    result = dictionnary.autocomplete(start_with)
    body = {
        "words" : result[0:MAX_AUTOCOMPLETE_RESULTS],
        "count" : len(result),
        "truncated_result" : len(result) > MAX_AUTOCOMPLETE_RESULTS
    }

    return jsonify(body)

@app.route('/<string:word>', methods=['GET'])
def check_word(word):
    if dictionnary.is_present(word):
        body = { "found": True, "word": word, "length": len(word) }
    else:
        body = { "found": False, "word": word, "error": 'word not found' }

    return jsonify(body)
