import sys
import random
global Q_table
class Player():
    hand = []
    state = 1 #1:同じ数字のみを出せる状態, 2:一つ大きい数字のみを出せる状態 3:2種類出せる状態, 4:何も出せない状態, 5:終了状態, 6:上がった状態
    black_set = 0#=set単位のblack
    white_set = 0#set単位のwhite
    black_game = 0#game単位のblack
    white_game = 0#game単位のwhite

def eqplusChange(field):#eq,plusを算出する
    eq = 0
    plus = 0
    if field == 0:
        eq = 0
        plus = 1
    elif field == 1:
        eq = 1
        plus = 2
    elif field == 2:
        eq = 2
        plus = 3
    elif field == 3:
        eq = 3
        plus = 0
    else:
        print("エラー")
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

def playCard(pl,lama_deck,field,eq,plus):#行動選択
    deck = lama_deck#デッキ
    fi = field#
    x = 0#ループ用
    while x < 1:#行動選択するまで終了しないために
        print("入力:0:降り,1:カードを出す2:カードを引く,3:何もしない(デバッグ用)")
        print(pl.hand)
        a = input()#行動選択
        if int(a) == 0:#降り
            fold(pl)
            x = 1
        elif int(a) == 1:#カードを出す
            if pl.state == 4:
                print("それはできません")
            else:
                print("カード")
                print(pl.hand)
                y = 0
                while y < 1:#エラー処理
                    b = input()#配列の位置を選択
                    if (pl.hand[int(b)] == eq) | (pl.hand[int(b)] == plus):#出せるかどうか
                        y = 1
                    else:
                        print("それは出せません")
                fi = pl.hand[int(b)]
                pl.hand.pop(int(b))
                x = 1
        elif int(a) == 2:#
            if len(deck) == 0:#
                print("それはできません")
            else:#
                x = deck.pop(0)
                pl.hand.append(x)
                pl.hand.sort()
                x = 1
    return deck, fi

def randomact(pl,lama_deck,field,eq,plus):
    x = 0
    deck = lama_deck
    fi = field
    while(x == 0):
        act = random.randint(1,100)#1:降りる,2:同じ数字を出す,3:次の数字を出す,4:カードを引く
        if(act%4 == 1):
            fold(pl)
            x = 1
        elif(act%4 == 2):
            if pl.state == 1 | pl.state == 3:
                pl.hand.pop(pl.hand.index(fi))
                x = 1
        elif(act%4 == 3):
            if pl.state == 2 | pl.state == 3:
                fi = plus
                pl.hand.pop(pl.hand.index(fi))
                x = 1
        else:
            if len(deck) != 0:
                x = deck.pop(0)
                pl.hand.append(x)
                pl.hand.sort()
                x = 1
    return deck,fi

def canMove(s, a):
    if s >= 1 and s <= 6 and a >= 1 and a <= 4:
        if (s == 1 and a == 3) or (a == 0):
            return False
        elif (s == 2 and a == 2) or (a == 0):
            return False
        elif s == 3 and a == 0:
            return False
        elif (s == 4) and (a == 2 or a == 3):
            return False
        else:
            return True
    else:
        return False

def MinQ(Q, s):
    min = Q[s][0]
    act = 0
    for i in range(1, 4):
        if (min > Q[s][i]) and canMove(s, i):
            min = Q[s][i]
            act = i
    return act
def MaxQ(Q, s):
    max = Q[s][0]
    act = 0
    for i in range(1, 4):
        if (max < Q[s][i]) and canMove(s, i):
            max = Q[s][i]
            act = i
    return act

# ε-Greedy選択
def eGreedy(Q, s, ipusiron, pl):
    if random.random() < 1-ipusiron:	# 確率1-eでgreedy
        return MaxQ(Q, pl.state)
    else:			# 確率eでランダム
        return random.randint(0, 3)

def Q_learning(pl,lama_deck,field,eq,plus):
    #1:同じ数字 2:一つ大きい数字 3:2種類 4:何も出せない 5:終了状態, 6:上がった状態
    x = 0
    ipusiron = 0.1
    ganma = 0.99
    arufa = 0.3
    s = pl.state
    deck = lama_deck
    
    fi = field
    setP = (pl.black_set * 5 + pl.white_set)
    while x == 0:
        act = eGreedy(Q_table, s, ipusiron, pl)
        if(act == 1):
            if (canMove(s,act)):
                fold(pl)
                x = 1
        elif(act == 2):
            if (canMove(s,act)):
                y = pl.hand.index(fi)
                pl.hand.pop(y)
                x = 1
        elif(act == 3):
            if (canMove(s,act)):
                fi = plus
                y = pl.hand.index(fi)
                pl.hand.pop(y)
                x = 1
        else:
            if len(deck) != 0:
                x = deck.pop(0)
                pl.hand.append(x)
                pl.hand.sort()
                x = 1
    #count = 0
    reward = 0
    #for i in pl.hand:
        #count += 1
        #reward += i
    
    setpointUpdate(pl)
    reward = setP-(pl.black_set * 5 + pl.white_set)
    s2 = pl.state
    act2 = eGreedy(Q_table, s, ipusiron, pl)
    Q_table[s][act] = (1 - arufa) * Q_table[s][act] + arufa * (reward + ganma * Q_table[s2][act2])
    return deck,fi


#ココからメイン
if __name__ == '__main__':
    global lama_deck #デッキ
    Q_table = [[0 for i in range(4)] for j in range(7)]
    Q_table[1][3] = -1000
    Q_table[2][2] = -1000
    Q_table[4][2] = -1000
    Q_table[4][3] = -1000
    field = 0 #場の数
    eq = 0 #stateを出すときに使う．fieldと同じ数
    plus = 0 #stateを出すときに使う．eqの一つ次の数
    lama_deck=[]
    playcount = 1000 #回すゲーム数
    i = 0 #
    path='result.csv'
    fo=open(path,'w')
    result = ""
    winner = 0
    before = 0
    #下からゲームスタート
    while i < playcount:
        player1 = Player()
        player2 = Player()
        while(gameFinish(player1,player2)):
            box = initialize(player1, player2,lama_deck,field)#初期化
            lama_deck = box[0]
            field = box[1]
            while(isFinish(player1,player2)):
                eqplus = eqplusChange(field)#eqとplusの値を算出
                eq = eqplus[0]
                plus = eqplus[1]
                stateUpdate(player1,player2,eq,plus)
                if player1.state < 5:#降りていないかの確認
                    #print("場の数" )
                    #print(field)
                    #print("先手")
                    box = Q_learning(player1,lama_deck,field,eq,plus)
                    lama_deck = box[0]
                    field = box[1]
                setpointUpdate(player1)
                eqplus = eqplusChange(field)
                eq = eqplus[0]
                plus = eqplus[1]
                stateUpdate(player1,player2,eq,plus)
                if(isFinish(player1,player2)):#先手側が上がっていた時にプレイできないようにするため
                    if player2.state < 5:#降りていないかの確認
                        #print("場の数" )
                        #print(field)
                        #print("後手")
                        box = randomact(player2,lama_deck,field,eq,plus)
                        lama_deck = box[0]
                        field = box[1]
                setpointUpdate(player2) 
            gamepointUpdate(player1)
            gamepointUpdate(player2)
            if len(player1.hand) == 0:
                pointMinus(player1)#上がっていたら一枚減らす
            if len(player2.hand) == 0:
                pointMinus(player2)#上がっていたら一枚減らす
        LastPoint1 = player1.black_game * 5 + player1.white_game
        LastPoint2 = player2.black_game * 5 + player2.white_game
        i += 1
        #result+=str(LastPoint1)+","+str(LastPoint2)+"\n"
        if LastPoint1 < LastPoint2:
            winner+=1
        result+=str(winner/i)+"\n"
        if i%1000 == 0:
            result+=str((winner-before)/1000)+'\n'
            before = winner
    fo.write(result)
    fo.close()