# import konlpy
import nltk
import socket
import json

def getETRI(text):
    if text == "":
        print("ETRI input with blank string")
        return None
    host = '143.248.135.146'
    port = 44444
    ADDR = (host, port)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect(ADDR)
    except KeyboardInterrupt:
        return None
    except Exception:
        print("ETRI connection failed")
        return None
    try:
        clientSocket.sendall(str.encode(text))
        buffer = bytearray()
        while True:
            data = clientSocket.recv(4096)
            if not data:
                break
            buffer.extend(data)
        result = json.loads(buffer.decode(encoding='utf-8'))

        return result
    except KeyboardInterrupt:
        return None
    except Exception:
        print("ETRI connection lost")
        return None
    finally:
        clientSocket.close()


def get_pos_list(json_data):
    sentence_dict = json_data["sentence"][0]
    morp_array = sentence_dict["morp"]
    ne_array = sentence_dict["NE"]

    ne_list = []
    for item in ne_array:
        text = item["text"]
        type = item["type"]
        begin = item["begin"]
        end = item["end"]
        if begin == end:
            continue
        ne_tuple = (text, type, begin, end)
        ne_list.append(ne_tuple)

    morp_list = []
    for item in morp_array:
        lemma = item["lemma"]
        type = item["type"]
        morp_tuple = (lemma, type)
        morp_list.append(morp_tuple)

    idx = 0
    for ne in ne_list:
        begin = ne[2]
        end = ne[3]
        temp_list = morp_list[begin - idx:end + 1 - idx]
        for temp in temp_list:
            morp_list.remove(temp)
        morp_list.insert(begin - idx, (ne[0], "NNP"))
        idx = idx + end - begin

    return morp_list


def get_chunk_tree(sentence):
    etri_out_json = getETRI(sentence)
    words = get_pos_list(etri_out_json)

    # Define a chunk grammar, or chunking rules, then chunk
    grammar = """
    VP: {<VCP|VV> <E.*|V.*>+ <VV|VX>}
    VP: {<VCP|VV> <E.*> <J.*>* <VV|VX>}
    VP: {<VV|VCP|VA|VCN|VX>+ <EP|EC>? <VX>?}
    VP: {<N.*>+ <XSV> <ETN> <JX> <VX>}
    VP: {<N.*>+ <XSV> <EP>*}
    VP: {<N.*>+ <XSA> <EP|EF|EC>* <VX>?} 
    NP: {<MM|MAG|SN|N.*>* <JKG|JC>* <N.*>+ <XSN>? <XSV>?}
    NP: {<MM|MAG|SN|N.*>* <VP|NP|AP> <XS.*>* <EP>* <ETM|ETN> <N.*>+ <XSN>?}
    NP: {<NP> <MAJ|NP>+}
    NP: {<NP>{2,}}
    E: {<E.*>* <S.*>*}
    J: {<J.*>+}
    M: {<M.*>}
    X: {<X.*>}
    I: {<I.*>}
    """

    parser = nltk.RegexpParser(grammar)
    chunks = parser.parse(words)
    # print("# Print whole tree")
    # print(chunks.pprint())

    # for subtree in chunks.subtrees():
    #     if subtree.label()!='NP' and subtree.label()!='VP' and subtree.label()!='J' and subtree.label()!='E' and subtree.label()!='AP' and subtree.label()!='MAJ'  and subtree.label()!='XPN'and subtree.label()!='S':
    #         # print(' '.join((e[0] for e in list(subtree))))
    #         print(subtree.pprint())

    return chunks




