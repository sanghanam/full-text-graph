from nltk import Tree

from src import processor as p
# from src import kbox_loader as kl
from src import rest_call as rc
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import json


def node_in_list(target, nodes):
    for node in nodes:
        s_open = node["s_open"]
        s_close = node["s_close"]
        t_open = target["s_open"]
        t_close = target["s_close"]
        if s_open == t_open and s_close == t_close:
            return True, node["id"]
    return False, -1


def get_full_text_graph(text, do_Frame, do_L2K):

    result = {}

    ## KBox
    # kbox = kl.load()

    ## SurfaceGraph
    print("======== Surface Graph =======")
    surface = rc.call_surface(text)
    # for triplet in surface:
    #     for triple in triplet:
    #         print(triple[0], triple[1], triple[2])

    nodes = []
    edges = []
    id = 0
    triples = surface["triples"]
    for triple in triples:

        head_list = []
        tail_list = []

        s = Tree.fromstring(triple["s"])
        for idx, n in enumerate(s):
            node = {}
            lex, pos, s_open, s_close = n.split("/")
            node["id"] = id
            node["lex"] = lex
            node["sem"] = "NIL"
            node["ont"] = "NIL"
            node["pos"] = pos
            node["s_open"] = s_open
            node["s_close"] = s_close
            exist, exist_id = node_in_list(node, nodes)
            if exist:
                head_list.append(exist_id)
            else:
                if idx == 0:
                    edge = {}
                    temp_list = []
                    temp_list.append(id)
                    edge["head"] = temp_list
                else:
                    temp_list = []
                    temp_list.append(id)
                    edge["tail"] = temp_list
                    edge["sem"] = "NIL"
                    edge["lex"] = "NIL"
                    edge["pos"] = "NIL"
                    edge["s_open"] = -1
                    edge["s_close"] = -1
                    edges.append(edge)
                    edge = {}
                    temp_list = []
                    temp_list.append(id)
                    edge["head"] = temp_list
                nodes.append(node)
                head_list.append(id)
                id = id + 1

        o = Tree.fromstring(triple["o"])
        for idx, n in enumerate(o):
            node = {}
            lex, pos, s_open, s_close = n.split("/")
            node["id"] = id
            node["lex"] = lex
            node["sem"] = "NIL"
            node["ont"] = "NIL"
            node["pos"] = pos
            node["s_open"] = s_open
            node["s_close"] = s_close
            exist, exist_id = node_in_list(node, nodes)
            if exist:
                tail_list.append(exist_id)
            else:
                if idx == 0:
                    edge = {}
                    temp_list = []
                    temp_list.append(id)
                    edge["head"] = temp_list
                else:
                    temp_list = []
                    temp_list.append(id)
                    edge["tail"] = temp_list
                    edge["sem"] = "NIL"
                    edge["lex"] = "NIL"
                    edge["pos"] = "NIL"
                    edge["s_open"] = -1
                    edge["s_close"] = -1
                    edges.append(edge)
                    edge = {}
                    temp_list = []
                    temp_list.append(id)
                    edge["head"] = temp_list
                nodes.append(node)
                tail_list.append(id)
                id = id + 1

        p = Tree.fromstring(triple["p"])
        lex, pos, s_open, s_close = p[0].split("/")
        edge = {}
        edge["lex"] = lex
        edge["sem"] = "NIL"
        edge["pos"] = pos
        edge["s_open"] = s_open
        edge["s_close"] = s_close
        edge["head"] = head_list
        edge["tail"] = tail_list
        edges.append(edge)

    result["docID"] = 0
    result["senID"] = 0
    result["vertex"] = nodes
    result["edge"] = edges

    print(json.dumps(result, ensure_ascii=False))

    return result

    # ## FrameNet
    # if do_Frame:
    #     print("======= FrameNet Graph =======")
    #     frame = rc.call_frame(text)
    #     print(frame)
    #     print("==============================")
    #     print()
    #
    # ## L2K
    # entity_dict = {}
    # if do_L2K:
    #     print("======== L2K Triples =========")
    #     l2k = rc.call_l2k(text)
    #     EL = l2k["EL"]
    #     sentence = EL["sentence"][0]
    #     ELU = sentence["ELU"]
    #     entities = ELU["entities"]
    #
    #     for entity in entities:
    #         text = entity["text"]
    #         uri = entity["uri"].replace("http://kbox.kaist.ac.kr/resource/", "")
    #         entity_dict[text] = uri
    #
    #     print(entity_dict)
    #
    #     PL = l2k["PL"]
    #     triples = PL["triples"]
    #
    #     for triple in triples:
    #         print(triple["s"], triple["p"], triple["o"], triple["sco"])
    #     print("==============================")
    #     print()

    ## Full-text Graph
    # surface_G = nx.DiGraph()
    #
    # for triplet in surface:
    #     prev_rel = ""
    #     for triple in triplet:
    #         sbj = triple[0]
    #         rel = triple[1]
    #         obj = triple[2]
    #
    #         splitted_sbj_list = []
    #         sbj_label = sbj._label
    #         for subtree in sbj.subtrees():
    #             for surface, pos_label in list(subtree):
    #                 uri = entity_dict.get(surface, "NOTIN")
    #                 if uri is "NOTIN":
    #                     splitted_sbj_list.append([surface, pos_label, False])
    #                 else:
    #                     splitted_sbj_list.append([uri, pos_label, True])
    #
    #         relation = ""
    #         if rel is not False:
    #             rel_label = rel._label
    #             for subtree in rel.subtrees():
    #                 for surface, pos_label in list(subtree):
    #                     relation = relation + " " + surface
    #             relation = relation.strip()
    #         if len(relation) == 0:
    #             relation = False
    #
    #         splitted_obj_list = []
    #         if obj is not False:
    #             obj_label = obj._label
    #             for subtree in obj.subtrees():
    #                 for surface, pos_label in list(subtree):
    #                     uri = entity_dict.get(surface, "NOTIN")
    #                     if uri is "NOTIN":
    #                         splitted_obj_list.append([surface, pos_label, False])
    #                     else:
    #                         splitted_obj_list.append([uri, pos_label, True])
    #
    #         if "J" in rel_label or relation is False:
    #             remain = ""
    #             for obj, o_label, is_uri in splitted_obj_list:
    #                 if is_uri:
    #                     surface_G.add_edge(prev_rel, obj, type="surface", surface=relation)
    #                 else:
    #                     # TODO: JKG handling...
    #                     remain = remain + " " + obj
    #                     if "J" in o_label:
    #                         continue
    #             remain = remain.strip()
    #             surface_G.add_edge(prev_rel, remain, type="surface", surface=relation)
    #         else:
    #             remain = ""
    #             for sbj, label, is_uri in splitted_sbj_list:
    #                 if is_uri:
    #                     surface_G.add_node(sbj, type="entity", label=label)
    #                 else:
    #                     remain = remain + " " + sbj
    #             remain = remain.strip()
    #             if len(remain) > 0:
    #                 surface_G.add_node(remain, type="surface", label="NP")
    #
    #             remain = ""
    #             for obj, label, is_uri in splitted_obj_list:
    #                 if is_uri:
    #                     surface_G.add_node(obj, type="entity", label=label)
    #                 else:
    #                     remain = remain + " " + obj
    #             remain = remain.strip()
    #             if len(remain) > 0:
    #                 surface_G.add_node(remain, type="surface", label="NP")
    #
    #             surface_G.add_node(relation, type="surface", label=rel_label)
    #             for sbj, s_label, is_uri in splitted_sbj_list:
    #                 surface_G.add_edge(sbj, relation, type="surface")
    #             for obj, o_label, is_uri in splitted_obj_list:
    #                 surface_G.add_edge(relation, obj, type="surface")
    #             prev_rel = relation
    # if rel_label == "J":
    #     surface_G.add_edge(tagged_sbj, tagged_obj, type="surface", surface=rel_surface)
    # else:
    #     surface_G.add_node(rel_surface, type="surface", label=rel_label)
    #     if len(tagged_sbj) != 0:
    #         surface_G.add_edge(tagged_sbj, rel_surface, type="surface")
    #     for entity in splitted_sbj_list:
    #         surface_G.add_edge(entity[0], rel_surface, type="surface")
    #
    #     if len(tagged_obj) != 0:
    #         surface_G.add_edge(rel_surface, tagged_obj, type="surface")
    #     for entity in splitted_obj_list:
    #         surface_G.add_edge(rel_surface, entity[0], type="surface")

    # entity_tagged_surface_graph.append([tagged_sbj.strip(), rel_surface.strip(), tagged_obj.strip()])

    # if do_Frame:
    #     frame_G = nx.DiGraph()
    #
    #     frdf = frame
    #     frame_index_set = []
    #     for rdf in frdf:
    #         f_index = rdf[0].replace("frame:", "").replace("-input_sent", "")
    #         f_arg = rdf[1].replace("frame:", "")
    #         f_arg = f_arg[f_arg.find("-") + 1:len(f_arg)]
    #         lu = rdf[2].replace("\"", "")
    #         # lu = lu[0:lu.find("^^")]
    #
    #         uri = entity_dict.get(lu, lu)
    #
    #         frame_G.add_node(uri, type="frame")
    #         frame_G.add_node(f_index, type="frame")
    #
    #         if f_index not in frame_index_set:
    #             frame_G.add_edge(uri, f_index, type="frame", label=f_arg)
    #             frame_index_set.append(f_index)
    #         else:
    #             frame_G.add_edge(f_index, uri, type="frame", label=f_arg)
    #
    #     # print(frame_G.nodes(data=True))
    #     # print(frame_G.edges(data=True))
    #
    # if do_L2K:
    #     ontology_G = nx.DiGraph()
    #
    #     for triple in triples:
    #         score = triple["sco"]
    #         if float(score) < 0.8:
    #             continue
    #
    #         sbj = triple["s"][0:triple["s"].find("/")]
    #         prop = triple["p"]
    #         obj = triple["o"][0:triple["o"].find("/")]
    #
    #         ontology_G.add_node(sbj, type="entity")
    #         ontology_G.add_node(prop, type="property")
    #         ontology_G.add_node(obj, type="entity")
    #         ontology_G.add_edge(sbj, prop, type="ontology")
    #         ontology_G.add_edge(prop, obj, type="ontology")
    #
    #     # print(ontology_G.edges(data=True))
    #
    # if do_Frame:
    #     surface_G = nx.compose(surface_G, frame_G)
    # if do_L2K:
    #     surface_G = nx.compose(surface_G, ontology_G)
    #
    # print("====== Full-text Graph =======")
    # print(surface_G.nodes(data=True))
    # print(surface_G.edges(data=True))

    # # plt.rc('font', family='NanumBarunGothicOTF')
    #
    # pos = nx.layout.spring_layout(surface_G)
    #
    # # node_sizes = [3 + 10 * i for i in range(len(surface_G))]
    # M = surface_G.number_of_edges()
    # # edge_colors = range(2, M + 2)
    # # edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
    #
    # # nx.draw(surface_G, with_labels=True)
    #
    # nodes = nx.draw_networkx_nodes(surface_G, pos, node_size=10, node_color='blue')
    # edges = nx.draw_networkx_edges(surface_G, pos, node_size=10, arrowstyle='->',
    #                                arrowsize=10, edge_color='black',
    #                                edge_cmap=plt.cm.Blues, width=2)
    # labels = nx.draw_networkx_labels(surface_G, pos, font_size=10, font_family='NanumGothic')
    # # set alpha value for each edge
    # # for i in range(M):
    # #     edges[i].set_alpha(edge_alphas[i])
    #
    # # pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
    # # pc.set_array(edge_colors)
    # # plt.colorbar(pc)
    #
    #
    #
    # ax = plt.gca()
    # ax.set_axis_off()
    # # plt.interactive(False)
    # plt.show()
    #
    # print("==============================")
    # print()


# text = "한지운은 9회초 타석에 들어섰으나 송승준에게 사구를 맞았다."
text = "민간 기업 스페이스X가 30일 미국 항공우주국 소속 우주 비행사 2명을 유인 우주선 크루 드래건으로 우주로 쏘아 올렸다."
# text = "국가보안위원회는 1954년부터 1991년까지 존속했던 소련의 정보 기관이다."
# text = "근우회는 1927년에 조직된 한국의 여성 단체이다."
# text = "쿠바에서 몇년간 생활을 했고, 말년에는 피델 카스트로와도 알고 지내는 사이였기 때문에 관광업의 비중이 높아진 뒤의 쿠바에서는 허밍웨이를 체 게바라와 함께 관광상품으로 써먹고 있다."

get_full_text_graph(text, False, False)
