# ���s��Q�l���ŏ��ƂȂ�s��act��Ԃ�
def MinQ(Q, s):
    min = Q[s, 0]
    act = 0
    for i in range(1, 4):
        if (min > Q[s, i]) and canMove(s, i):
            min = Q[s, i]
            act = i
    return act

# ��-Greedy�I��
def eGreedy(Q, s, e):
    if random.random() < 1-e:	# �m��1-e��greedy
        return MinQ(Q, pl.state)
    else:			# �m��e�Ń����_��
        return random.randint(0, 3)