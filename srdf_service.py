from flask import Flask, request, jsonify
import jpype
import processor as p
from nltk.tree import Tree
# from src import full_text_graph_generator as fg

app = Flask(__name__)

print("Start JVM")
jpype.startJVM(jpype.getDefaultJVMPath())
@app.route("/surface-parser", methods=["POST"])
def full_text():
    jpype.attachThreadToJVM()
    data = request.get_json()
    text = data["text"]
    surface = p.single_processor(text)
    json_triples = []
    result = {}
    print_triples = []
    for triplet in surface:
        for triple in triplet:
            json_triple = {}
            json_triple["s"] = ' '.join(str(triple[0]).split())
            json_triple["p"] = ' '.join(str(triple[1]).split())
            json_triple["o"] = ' '.join(str(triple[2]).split())
            print_triple = Tree('T', [triple[0], triple[1], triple[2]])
            json_triples.append(json_triple)
            print_triples.append(print_triple)
    result["triples"] = json_triples

    for print_triple in print_triples:
        print_triple.pretty_print()

    return jsonify(result)

app.run(host="kbox.kaist.ac.kr", port="47361")