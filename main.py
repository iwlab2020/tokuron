import sys
import random

class Player():
    hand = []
    state = 1      #1:同じ数字のみを出せる状態, 2:一つ大きい数字のみを出せる状態 3:2種類出せる状態, 4:何も出せない状態, 5:終了状態, 6:上がった状態
    black_set = 0  #=set単位のblack
    white_set = 0  #set単位のwhite
    black_game = 0 #game単位のblack
    white_game = 0 #game単位のwhite

def eqplusChange(field):#eq,plusを算出する
    eq = field
    plus = (eq + 1) % 4
    return eq,plus

def stateJudge(pl,eq,plus):
    if len(pl.hand) == 0:#上がっている状態
        pl.state = 6
    elif pl.state == 5:#降りている状態
        state = 5
    elif eq in pl.hand:
        if plus in pl.hand:#2種類出せる状態
            pl.state = 3
        else:#同じ数のみ出せる状態
            pl.state = 1
    elif plus in pl.hand:#1つ大きい数字のみ出せる状態
        pl.state = 2
    else:#何も出せない状態
        pl.state = 4

def stateUpdate(pl1,pl2,eq,plus):
    stateJudge(pl1,eq,plus)
    stateJudge(pl2,eq,plus)

def exchange(black,white):#black,whiteを両替する
    a = divmod(white,5)
    bl = black + a[0]
    wh = a[1]
    return bl,wh

def pointManage(pl):#handに対する点数
    black = 0
    white = 0
    #それぞれのカードがhandにあるか確認
    if 0 in pl.hand:
        black += 1
    if 1 in pl.hand:
        white += 1
    if 2 in pl.hand:
        white += 2
    if 3 in pl.hand:
        white += 3
    a = exchange(black,white)
    black = a[0]
    white = a[1]
    return black, white

def setpointUpdate(pl):#set中のpointを更新
    point = pointManage(pl)
    pl.black_set = pl.black_game + point[0]
    pl.white_set = pl.white_game + point[1]

def gamepointUpdate(pl):#game中のpointを更新
    pl.black_game = pl.black_set
    pl.white_game = pl.white_set

def initialize(pl1,pl2,lama_deck,field):#初期化
    lama_deck=[0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3]#デッキのリセット
    random.shuffle(lama_deck)#デッキのシャッフル
    hand1=[]#1の手札を保存
    hand2=[]#2の手札を保存
    for i in range(4):#手札を配る
        hand1.append(lama_deck.pop(0))
        hand2.append(lama_deck.pop(0))
    pl1.hand=hand1#手札を代入
    pl2.hand=hand2#手札を代入
    pl1.hand.sort()#手札の並び替え
    pl2.hand.sort()#手札の並び替え
    pl1.state = 0#stateを0で初期化
    pl2.state = 0#stateを0で初期化
    field = lama_deck.pop(0)#デッキの一番上を場に出す
    return lama_deck,field

def pointMinus(pl):#上がったときに点数を下げる
    if pl.black_game != 0:
        pl.black_game -= 1
    elif pl.white_game != 0:
        pl.white_game -= 1

def fold(pl):#降りる関数
    pl.state = 5

def isFinish(pl1,pl2):#setの終了判定
    if (pl1.state == 5) & (pl2.state == 5):#両方降りているか
        return False
    elif (pl1.state == 6) | (pl2.state == 6):#どちらか上がっていないか
        return False
    else:
        return True

def gameFinish(pl1,pl2):#gameの終了判定
    pl1point = pl1.black_game * 5 + pl1.white_game
    pl2point = pl2.black_game * 5 + pl2.white_game
    if (pl1point < 20) & (pl2point < 20):#どちらとも20点を超えていないかどうか
        return True
    else:
        return False

def canMove(s, a):
    if s >= 1 and s <= 6 and a >= 1 and a <= 4:
        if a == 0:
            if s == 4 or s == 5 or s == 6: return False
            else: return True
        if a == 1:
            if s == 1: return True
            else: return False
        elif a == 2:
            if s == 2: return True
            else: return False
        elif a == 3:
            if s == 1 or s == 2 or s == 3 or s == 4: return True
            else: return False
        else:
            return False
    return False

def eGreedy(Q, s, e):
    if random.random() < 1-e:
        #print("s = ", s)
        min = Q[s][0]
        act = 0
        for i in range(4):
            if canMove(s, i) and (min > Q[s][i]):
                min = Q[s][i]
                act = i
        #print("act = ", act)
        return act
    else:
        return randhand(s)

def randhand(s):
    act = random.randint(0, 3)
    while canMove(s, act) == False:
        act = random.randint(0, 3)
    return act

# Action 0：降りる，1：fieldを出す，2：nextを出す，3：引く
def doAction(pl, deck, field, act):
    #print('act = ', act)
    #print('field = ', field)
    #print('state = ', pl.state)
    next = (field + 1) % 4
    if act == 0:
        fold(pl)
    elif act == 1:
        i_next = pl.hand.index(field)
        field = pl.hand[i_next]
        #pl.hand.pop(i_next)
        pl.hand.remove(field)
    elif act == 2:
        i_next = pl.hand.index(next)
        field = pl.hand[i_next]
        #pl.hand.pop(i_next)
        pl.hand.remove(field)
    elif act == 3:
        if len(deck) == 0:
            fold(pl)
        else: 
            x = deck.pop(0)
            pl.hand.append(x)
            pl.hand.sort()
    
    return deck, field

#ココからメイン
if __name__ == '__main__':
    Q = [[0 for j in range(4)] for i in range(7)] #Qtable
    SumReward = [[0 for j in range(4)] for i in range(7)] #累積報酬テーブル
    RewardCount = [[0 for j in range(4)] for i in range(7)] #報酬獲得回数テーブル
    Rules = []
    e = 0
    global lama_deck #デッキ
    field = 0 #場の数
    eq = 0 #stateを出すときに使う．fieldと同じ数
    plus = 0 #stateを出すときに使う．eqの一つ次の数
    lama_deck=[]
    playcount = 1000000 #回すゲーム数
    winrates = []
    wincount = 0
    i = 0 #
    #下からゲームスタート
    while i < playcount:
        player1 = Player()
        player2 = Player()
        while(gameFinish(player1,player2)):
            box = initialize(player1, player2,lama_deck,field) #初期化
            lama_deck = box[0]
            field = box[1]
            #setのループ
            episode = 0
            while(isFinish(player1,player2)):
                eqplus = eqplusChange(field) #eqとplusの値を算出
                eq = eqplus[0]
                plus = eqplus[1]
                stateUpdate(player1,player2,eq,plus)
                if player1.state < 5: #降りていないかの確認
                    #print("場の数" )
                    #print(field)
                    #print("先手")
                    #box = playCard(player1,lama_deck,field,eq,plus)
                    act = randhand(player1.state)
                    lama_deck, field = doAction(player1, lama_deck, field, act)
                    #lama_deck = box[0]
                    #field = box[1]
                setpointUpdate(player1)
                eqplus = eqplusChange(field)
                eq = eqplus[0]
                plus = eqplus[1]
                stateUpdate(player1,player2,eq,plus)
                if(isFinish(player1,player2)): #先手側が上がっていた時にプレイできないようにするため
                    s = player2.state
                    if s < 5: #降りていないかの確認
                        #print("場の数" )
                        #print(field)
                        #print("後手")
                        #box = playCard(player2,lama_deck,field,eq,plus)
                        act = eGreedy(Q, s, e)
                        lama_deck, field = doAction(player2, lama_deck, field, act)
                        Rules.append([s, act])
                        #lama_deck = box[0]
                        #field = box[1]
                        stateUpdate(player1, player2, field, (field+1) % 4)
                        episode += 1
                setpointUpdate(player2)
            # セットポイントの計算
            point1 = player1.black_set * 5 + player1.white_set
            point2 = player2.black_set * 5 + player2.white_set
            # Player2が負けなら報酬
            if point1 > point2:
                for t in range(episode):
                    RewardCount[Rules[t][0]][Rules[t][1]] += 1
                    SumReward[Rules[t][0]][Rules[t][1]] -= point2
                    Q[Rules[t][0]][Rules[t][1]] = SumReward[Rules[t][0]][Rules[t][1]] / RewardCount[Rules[t][0]][Rules[t][1]]
            gamepointUpdate(player1)
            gamepointUpdate(player2)
            #print(player1.hand)
            if len(player1.hand) == 0:
                pointMinus(player1)#上がっていたら一枚減らす
            if len(player2.hand) == 0:
                pointMinus(player2)#上がっていたら一枚減らす

        if (player1.black_game * 5 + player1.white_game) > (player2.black_game * 5 + player2.white_game):
            wincount += 1
        i += 1
        winrates.append((wincount/i)*100)

    
    with open('Monte_Carlo.csv', 'w') as w_file:
        for i in range(playcount):
            w_file.write(str(winrates[i]) + ',\n')
        

