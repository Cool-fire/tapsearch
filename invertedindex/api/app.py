from flask import Flask, jsonify, make_response, request, redirect, url_for, render_template
from invertedindex.search import processQuery, getDocumentText
from invertedindex.index import indexCorpus
from invertedindex.database import deleteDatabase
from itertools import islice
import os

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/search', methods=['GET'])
def get_documents():
    query = request.args.get('word')
    print(query)
    documents = []
    docs = processQuery(query)
    if not docs:
        return make_response(jsonify({'error': 'term Not found or might be a stoplist word'}), 200)
    else:
        top_docs = islice(docs.items(), 0, 10)
        for id, score in top_docs:
            text = getDocumentText(id)
            documents.append({"id": id, "score": score, "text": text})
        return jsonify({'documents': documents})


@app.route('/index', methods=['POST', 'GET'])
def insert_corpus():
    if request.method == 'POST':
        corpus = request.form.get('corpus')
        print(corpus)
        indexCorpus(corpus)
        print("corpus indexed")
        return redirect(url_for('search_render'))
    return render_template('index.html')


@app.route('/api/insert-json', methods=['POST'])
def insert_json():
    if request.method == 'POST':
        req_data = request.get_json()
        corpus = req_data['corpus']
        indexCorpus(corpus)
        return "corpus indexed"

@app.route('/clear', methods=['GET'])
def clear_render():
    return render_template('clear.html')


@app.route('/search', methods = ['GET'])
def search_render():
    return render_template('search.html')

@app.route('/api/clear', methods=['GET'])
def clear():
    if deleteDatabase():
        return "successfully deleted"
    return "error occured while deleting"


if __name__ == "__main__":
    print('test', os.getcwd())
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
