# import konlpy
import nltk
import rest_call as rc


def get_character_position_list(lemma_list, position_list):
    character_list = []
    byte_idx = -1
    start = -1
    for i, lemma in enumerate(lemma_list):
        if i == 0:
            start = 0
            byte_idx = 0
        end = start + len(lemma)
        character_list.append((int(start), int(end)))
        b = bytearray(lemma, 'utf-8')
        byte_idx = byte_idx + len(b)
        if i == len(lemma_list) - 1:
            return character_list
        byte_gap = (position_list[i + 1] - byte_idx)
        gap = byte_gap
        if byte_gap < 0:
            if byte_gap % 3 == 0:
               gap = byte_gap / 3
        byte_idx = byte_idx + byte_gap
        start = end + gap

def get_pos_list(json_data):
    sentence_dict = json_data["sentence"][0]
    morp_array = sentence_dict["morp"]
    ne_array = sentence_dict["NE"]

    lemma_list = []
    position_list = []

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
        lemma_list.append(lemma)
        type = item["type"]
        position = item["position"]
        position_list.append(position)
        morp_tuple = (lemma, type)
        morp_list.append(morp_tuple)

    character_list = get_character_position_list(lemma_list, position_list)

    morp_with_position_list = []
    for i, morp in enumerate(morp_list):
        start = character_list[i][0]
        end = character_list[i][1]
        morp_with_position_list.append((morp[0], morp[1], str(start), str(end)))

    idx = 0
    for ne in ne_list:
        begin = ne[2]
        end = ne[3]
        temp_list = morp_with_position_list[begin - idx:end + 1 - idx]
        open = -1
        close = -1
        for i, temp in enumerate(temp_list):
            if i == 0:
                open = temp[2]
            elif i == len(temp_list) - 1:
                close = temp[3]
            morp_with_position_list.remove(temp)
        morp_with_position_list.insert(begin - idx, (ne[0].replace(" ", "_"), "NNP", str(open), str(close)))
        idx = idx + int(end) - int(begin)

    return morp_with_position_list


def get_chunk_tree(sentence):
    etri_out_json = rc.getETRI(sentence)
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




