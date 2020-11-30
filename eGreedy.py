# 状態sのQ値が最小となる行動actを返す
def MinQ(Q, s):
    min = Q[s, 0]
    act = 0
    for i in range(1, 4):
        if (min > Q[s, i]) and canMove(s, i):
            min = Q[s, i]
            act = i
    return act

# ε-Greedy選択
def eGreedy(Q, s, e):
    if random.random() < 1-e:	# 確率1-eでgreedy
        return MinQ(Q, pl.state)
    else:			# 確率eでランダム
        return random.randint(0, 3)