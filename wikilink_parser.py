
def remove_linktext(sentence):
    start_index = 0
    end_index = 0
    bar = 0
    link_text_list = []
    while start_index < len(sentence):
        start_index = sentence.find('<link>', start_index)
        if start_index == -1:
            break
        end_index = sentence.find('</link>', start_index)
        link_text = sentence[start_index:end_index + 7]
        # print(link_text)
        bar = sentence.find('|', start_index)
        surface = sentence[start_index+6:bar]
        entity = sentence[bar + 1:end_index]
        # print(surface)
        # print(entity)
        link_text_list.append((link_text, surface))
        start_index += 1

    for item in link_text_list:
        sentence = sentence.replace(item[0], item[1])

    return sentence
