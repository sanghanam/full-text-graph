import csv

def load():

    kbox_triple_set = []

    f = open('../data/kbox/kbox_all.tsv', 'r', encoding='utf-8')
    rdr = csv.reader(f, delimiter='\t')
    for line in rdr:
        sbj = line[0]
        prop = line[1]
        obj = line[2]

        if "http://dbpedia.org/ontology/" not in prop or "http://ko.dbpedia.org/resource/" not in obj:
            continue

        sbj = sbj[1:len(sbj) - 1].replace("http://ko.dbpedia.org/resource/", "")
        prop = prop[1:len(prop) - 1].replace("http://dbpedia.org/ontology/", "")
        obj = obj[1:len(obj) - 1].replace("http://ko.dbpedia.org/resource/", "")

        triple = (sbj, prop, obj)
        print(triple)
        kbox_triple_set.append(triple)

    return kbox_triple_set

