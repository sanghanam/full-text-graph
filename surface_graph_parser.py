def get_lists(chunks):
    subject_list = []
    object_list = []
    relation_list = []
    exception_list = []
    # print(chunks.pprint())
    idx = 0
    for chunk in chunks:
        # prev_chunk = chunks[idx - 1][0]
        # if type(prev_chunk) is str:
        #     exception_list.append(prev_chunk)
        #     idx += 1
        #     continue
        if chunk._label == 'NP':
            if idx + 1 == len(chunks):
                return subject_list, relation_list, object_list, exception_list
            post_chunk = chunks[idx + 1]
            if str(post_chunk._label).startswith('J'):
                lemma = post_chunk[0][0]
                pos = post_chunk[0][1]
                if pos == 'JKS': # or pos == 'JX'
                    subject_list.append((chunk, post_chunk, idx))
                elif pos == 'JX' and (lemma == '는' or lemma == '은'):
                    subject_list.append((chunk, post_chunk, idx))
                else:
                    object_list.append((chunk, post_chunk, idx))
            elif str(post_chunk._label).startswith('E'):
                object_list.append((chunk, post_chunk, idx))
            else:
                object_list.append((chunk, False, idx))

        elif chunk._label == 'VP':
            post_chunk = chunks[idx + 1]
            if str(post_chunk._label).startswith('E'):
                relation_list.append((chunk, post_chunk, idx))

        idx += 1
    return subject_list, relation_list, object_list, exception_list

def make_triplet(subject_list, relation_list, object_list):
    graph = []
    triple_set = []
    main_exist = False
    marked_object_position = []
    print(subject_list)
    print(object_list)
    if len(subject_list) == 1 and len(relation_list) == 1 and len(object_list) == 0:
        subject = subject_list[0]
        relation = relation_list[0]
        s_body = subject[0]
        s_affix = subject[1]
        r_body = relation[0]
        triple_set.append((s_body, s_affix, r_body))
        # triple_set.append((s_body, r_body, False))
        graph.append(triple_set)

    elif len(subject_list) == 1 and len(relation_list) == 1 and len(object_list) == 1:
        subject = subject_list[0]
        relation = relation_list[0]
        object = object_list[0]
        s_body = subject[0]
        s_affix = subject[1]
        r_body = relation[0]
        o_body = object[0]
        o_affix = object[1]

        # if r_body[0][1] == 'VCP':
        #     triple_set.append((s_body, r_body, o_body))
        # else:
        triple_set.append((s_body, s_affix, r_body))
        triple_set.append((r_body, o_affix, o_body))
        graph.append(triple_set)

    elif len(subject_list) > 1 and len(object_list) > 1 and len(relation_list) == 1:
        relation = relation_list[0]
        main_exist = False
        r_position = relation[2]
        r_body = relation[0]
        r_affix = relation[1]

        for subject in reversed(subject_list):
            s_body = subject[0]
            s_affix = subject[1]
            s_position = subject[2]

            for a in r_affix:
                # print(a)
                if a[1] == 'EC' or a[1] == 'EF':  # 연결어미 / 종결어미 - 트리플 생성
                    for object in reversed(object_list):
                        if len(marked_object_position) > 0:
                            flag_position = min(marked_object_position)
                        else:
                            flag_position = 500
                        o_position = object[2]
                        o_affix = object[1]
                        o_body = object[0]
                        if s_position < o_position < flag_position:
                            if main_exist is False:
                                # if o_affix is not False and o_affix[0][1] == 'JKO' or r_body[0][1] == 'VCP':
                                triple_set.append((s_body, s_affix, r_body))
                                triple_set.append((r_body, o_affix, o_body))
                                # else:
                                #     triple_set.append((s_body, r_body, False))
                                #     triple_set.append((r_body, o_affix, o_body))
                                marked_object_position.append(object[2])
                                # print((subject, relation, object))
                                # main_exist = True
                                # main_rel = r_body
                            # else:
                            #     triple_set.append((main_rel, o_affix, o_body))
                            #     marked_object_position.append(o_position)
                                # print((main_rel, object[1], object))
        graph.append(triple_set)
    elif len(relation_list) == 0 and len(subject_list) > 0 and len(object_list) > 0:
        for subject in subject_list:
            s_body = subject[0]
            s_affix = subject[1]
            s_position = subject[2]
            end_object = object_list[len(object_list) - 1]
            main_exist = False
            if len(marked_object_position) > 0:
                flag_position = max(marked_object_position)
            else:
                flag_position = 0
            r_position = end_object[2] + 1 #o_poistion
            r_body = ('이', 'VCP')
            r_affix = False
            end_o_affix = end_object[1]
            if end_o_affix is False:
                print("TODO: handle this case - (1)")
                continue
            for a in end_o_affix:
                # print(a)
                if a[1] == 'EF':  # 연결어미 / 종결어미 - 트리플 생성
                    for object in reversed(object_list):
                        o_position = object[2]
                        o_affix = object[1]
                        o_body = object[0]
                        if o_position < r_position and o_position > flag_position:
                            if main_exist is False:
                                triple_set.append((s_body, s_affix, r_body))
                                triple_set.append((r_body, o_affix, o_body))
                                marked_object_position.append(object[2])
                                # print((subject, relation, object))
                                main_exist = True
                                main_rel = r_body
                            else:
                                triple_set.append((main_rel, o_affix, o_body))
                                marked_object_position.append(o_position)
                                # print((main_rel, object[1], object))
            graph.append(triple_set)
    elif len(subject_list) == 1 and len(relation_list) > 0 and len(object_list) > 0:
        subject = subject_list[0]
        s_body = subject[0]
        s_affix = subject[1]
        s_position = subject[2]
        for relation in relation_list:
            main_exist = False
            if len(marked_object_position) > 0:
                flag_position = max(marked_object_position)
            else:
                flag_position = 0
            r_position = relation[2]
            r_body = relation[0]
            r_affix = relation[1]
            for a in r_affix:
                # print(a)
                if a[1] == 'EC' or a[1] == 'EF':  # 연결어미 / 종결어미 - 트리플 생성
                    for object in reversed(object_list):
                        o_position = object[2]
                        o_affix = object[1]
                        o_body = object[0]
                        if o_position < r_position and o_position > flag_position:
                            if main_exist is False:
                                # if o_affix is not False and o_affix[0][1] == 'JKO' or r_body[0][1] == 'VCP':
                                triple_set.append((s_body, s_affix, r_body))
                                triple_set.append((r_body, o_affix, o_body))
                                # else:
                                #     triple_set.append((s_body, s_affix, r_body))
                                #     triple_set.append((r_body, o_affix, o_body))
                                marked_object_position.append(object[2])
                                # print((subject, relation, object))
                                main_exist = True
                                main_rel = r_body
                            else:
                                triple_set.append((main_rel, o_affix, o_body))
                                marked_object_position.append(o_position)
                                # print((main_rel, object[1], object))
        graph.append(triple_set)
    elif len(subject_list) > len(object_list):
        print("TODO: handle this case - len(subject_list) > len(object_list)")
    elif len(relation_list) > 1 and len(relation_list) > len(object_list) and len(subject_list) == 1:
        print(
            "TODO: handle this case - len(relation_list) > 1 and len(relation_list) > len(object_list) and len(subject_list) == 1")
    else:
        print("TODO: we cannot cover this sentence type yet...")

    return graph

def print_graph(graph):
    for triplet in graph:
        for triple in triplet:
            print(triple[0], triple[1], triple[2])
    print("============================== ")
    print("")


# sentence = u'그는 대다수의 작품을 1920년대 중반부터 1950년대 중반 사이에 발표하였고, 1954년에 노벨 문학상을 수상하였다.'
# chunks = c.get_chunk_tree(sentence)
# chunks.pprint()
# subject_list, relation_list, object_list, exception_list = get_lists(chunks)
#
# print("======== chunk to list (distributing roles) ======= ")
# print("sbj_list:", subject_list)
# print("rel_list:", relation_list)
# print("obj_list:", object_list)
# print("exp_list:", exception_list)
#
# graph = make_triplet(subject_list, relation_list, object_list)
# print_graph(graph)
