import sys
import random 
import numpy as np
import os

class Player():
    hand = []
    state = 1 #1:同じ数字のみを出せる状態, 2:一つ大きい数字のみを出せる状態 3:2種類出せる状態, 4:何も出せない状態, 5:終了状態, 6:上がった状態
    black_set = 0#=set単位のblack
    white_set = 0#set単位のwhite
    black_game = 0#game単位のblack
    white_game = 0#game単位のwhite

class RULE():
    def __init__(self,x,y):
        self.rstate = x
        self.action = y

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

def playCard(pl,lama_deck,field,eq,plus,R,episode):#行動選択(PS)
    deck = lama_deck#デッキ
    fi = field#
    x = 0#ループ用
    state = pl.state
    while x < 1:#行動選択するまで終了しないために
        #print("入力:0:降り,1:カードを出す2:カードを引く,3:何もしない(デバッグ用)")
        #print(pl.hand)
        #a = ActionSelect(pl.state)#行動選択
        a = random.randrange(3)
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
                    b = random.randrange(len(pl.hand))#配列の位置を選択
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
    R = RuleUpdate(state,a,episode)
    return deck, fi

def playCardRnd(pl,lama_deck,field,eq,plus):#行動選択(乱数)
    deck = lama_deck#デッキ
    fi = field#
    x = 0#ループ用
    while x < 1:#行動選択するまで終了しないために
        #print("入力:0:降り,1:カードを出す2:カードを引く,3:何もしない(デバッグ用)")
        #print(pl.hand)
        a = random.randrange(3)#行動選択(乱数)
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
                    b = random.randrange(len(pl.hand))#行動選択(乱数)#配列の位置を選択
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

def ActionSelect(state): #行動選択手法(softmaxでやろうかな，検討中)
    values = [0]*4  
    i=0
    #tau = 0.4 #温度パラメータ
    for i in range(4):
        values[i] = Q[i][state]
    #sum_exp_values = sum([np.exp(v/tau) for v in range(values)])
    #p = [np.exp(v/tau)/sum_exp_values for v in range(values)]      # 確率分布の生成
    #action = np.random.choice(np.arange(len(values)), p=p)  # 確率分布pに従ってランダムで選択
    #print(action)
    list.sort(values)
    return values[0]


def RuleUpdate(state,action,episode): #PSのルール更新
    R[episode].rstate = state
    R[episode].action = action
    print("Rテーブルのデバッグ："+str(R[episode].rstate)+":"+str(R[episode].action))
    return R

def QUpdate(Q,R,lastpoint): #PSのQtable更新
    Cbid = 1
    print("Rテーブルのデバッグ："+str(R[episode].rstate)+":"+str(R[episode].action)) 
    for i in range(episode):
        Q[R[i].action][R[i].rstate]=Q[R[i].action][R[i].rstate]+Cbid*(Q[R[i].action][R[i].rstate]-lastpoint)
    return Q

#ココからメイン
if __name__ == '__main__':
    global lama_deck #デッキ
    global Q
    global R
    global episode
    field = 0 #場の数
    eq = 0 #stateを出すときに使う．fieldと同じ数
    plus = 0 #stateを出すときに使う．eqの一つ次の数
    Cbid = 1
    lama_deck=[]
    Q=[[0]*7]*4 #Qtable
    LastPoint1 = 0
    LastPoint2 = 0
    playcount = 10 #回すゲーム数
    path='result.csv'
    fo=open(path,'w')
    result = ""
    i = 0 #
    #下からゲームスタート
    while i < playcount:
        R = [RULE(0,0)]*20
        LastPoint1 = 0
        LastPoint2 = 0
        episode = 0
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
                    print("場の数" )
                    print(field)
                    print("先手")
                    box = playCard(player1,lama_deck,field,eq,plus,R,episode)
                    lama_deck = box[0]
                    field = box[1]
                setpointUpdate(player1) 
                eqplus = eqplusChange(field)
                eq = eqplus[0]
                plus = eqplus[1]
                stateUpdate(player1,player2,eq,plus)
                if(isFinish(player1,player2)):#先手側が上がっていた時にプレイできないようにするため
                    if player2.state < 5:#降りていないかの確認
                        print("場の数" )
                        print(field)
                        print("後手")
                        box = playCardRnd(player2,lama_deck,field,eq,plus)
                        lama_deck = box[0]
                        field = box[1]
                setpointUpdate(player2)
                episode = episode + 1 
            gamepointUpdate(player1)
            gamepointUpdate(player2)
            print(player1.hand)
            if len(player1.hand) == 0:
                pointMinus(player1)#上がっていたら一枚減らす
            if len(player2.hand) == 0:
                pointMinus(player2)#上がっていたら一枚減らす
            LastPoint1 = player1.black_game * 5 + player1.white_game
            LastPoint2 = player2.black_game * 5 + player2.white_game
            print("先手のポイント")
            print(LastPoint1)
            print("後手のポイント")
            print(LastPoint2)
        Q=QUpdate(Q,R,LastPoint1)
        i += 1
        result+=str(LastPoint1)+","+str(LastPoint2)+"\n"
    print(Q)
    fo.write(result)
    fo.close()
        