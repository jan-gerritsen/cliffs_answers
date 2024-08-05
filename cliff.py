from flask import Flask, render_template, request

import rag_server
from load_data import clean_data, load_document_into_chroma
from delete_chroma_collection import delete_collection

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        # clean_data() # remove any old files

        # delete_collection('my_collection') # remove any old vector db data
        f = request.files['file']
        f.save(f'./data/{f.filename}')
        load_document_into_chroma()
        return render_template("ama.html", name=f.filename)


@app.route("/ama", methods=['POST'])
def ama():
    question = request.form.get("question")
    name = request.form.get("name")
    answer = rag_server.retrieve_and_respond(question)
    return render_template('ama.html', name=name, question=question, answer=answer)