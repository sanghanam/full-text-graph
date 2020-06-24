from flask import Flask, request, jsonify
import jpype
from src import processor as p
from nltk.tree import Tree
from src import full_text_graph_generator as fg

app = Flask(__name__)

print("Start JVM")
jpype.startJVM(jpype.getDefaultJVMPath())
@app.route("/full-parser", methods=["POST"])
def get_full_text():
    jpype.attachThreadToJVM()
    data = request.get_json()
    text = data["text"]
    full_text = fg.get_full_text_graph(text, False, False)

    return jsonify(full_text)

app.run(host="kbox.kaist.ac.kr", port="47362")