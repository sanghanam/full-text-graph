text = "들어섰으나 송승준에게 사구를 맞았다."
lemma_list = ["들어서", "었", "으나", "송승준", "에게", "사구", "를", "맞", "았", "다", "."]
position_list = [0, 6, 9, 16, 25, 32, 38, 42, 45, 48, 51]

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

character_list = get_character_position_list(lemma_list, position_list)
print(character_list)


