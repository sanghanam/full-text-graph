import csv
import re
import surface_graph_parser as sp
import chunking as c
import wikilink_parser as wp


def clean_text(text):
    cleaned = re.sub(r'\([^(^)]*\(*[^(^)]*\)*[^(^)]*\)', '', text).replace(' [', '').replace('] ', '').replace('_', ' ')
    # cleaned = re.sub(r'\([^)]*\)', '', cleaned)
    return cleaned

def dump_processor():
    wr = open('../data/surface_graph_log.txt', 'w', encoding='utf-8')
    f = open('../data/merged_abstract.tsv', 'r', encoding='utf-8')
    rdr = csv.reader(f, delimiter='\t')
    first_line = 0
    for line in rdr:
        if line[2] == '1':
            first_line += 1
            sentence = line[4].strip()
            sentence = wp.remove_linktext(sentence)
            cleaned_text = clean_text(sentence)
            wr.write(cleaned_text)
            chunks = c.get_chunk_tree(cleaned_text)
            # if chunks is False:
            #     continue
            wr.write(str(chunks.pprint()))
            subject_list, relation_list, object_list, exception_list = sp.get_lists(chunks)

            print(subject_list)
            print(relation_list)
            print(object_list)
            print(exception_list)

            wr.write("======== chunk to list (giving roles) ======= ")
            wr.write(subject_list.__str__())
            wr.write(relation_list.__str__())
            wr.write(object_list.__str__())
            wr.write(exception_list.__str__())

            graph = sp.make_triplet(subject_list, relation_list, object_list)
            sp.print_graph(graph)
            for triplet in graph:
                for triple in triplet:
                    wr.write(str(triple[0]) + "\t" + str(triple[1]) + "\t" + str(triple[2]))
            wr.write("")

    wr.close()

    print(first_line)


def single_processor(text):
    sentence = wp.remove_linktext(text)
    cleaned_text = clean_text(sentence)
    # print(cleaned_text)
    chunks = c.get_chunk_tree(cleaned_text)
    # if chunks is False:
    #     continue
    # print(chunks.pprint())
    subject_list, relation_list, object_list, exception_list = sp.get_lists(chunks)

    # print(subject_list)
    # print(relation_list)
    # print(object_list)
    # print(exception_list)

    graph = sp.make_triplet(subject_list, relation_list, object_list)
    # sp.print_graph(graph)

    return graph

