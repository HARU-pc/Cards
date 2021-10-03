############################################################################################
#トランプゲーム作成用のモジュール (ジョーカーなし)
############################################################################################

import numpy as np
import random


############################################################################################
#山札を作成


def Reset():  #list

    Deck = []

    Marks = [i for i in ["♥","♦","♠","♣"]*13]

    for i in range(52):
        Card_Num = int(i // 4 + 1)

        if Card_Num == 11:
            Card_Name = "Jack"
        elif Card_Num == 12:
            Card_Name = "Queen"
        elif Card_Num == 13:
            Card_Name = "King"
        elif Card_Num == 1:
            Card_Name = "Ace"
        else:
            Card_Name = str(Card_Num)

        Deck.append([Marks[i],Card_Num,Card_Name])


    return Deck


def Reset_np():  #Numpy配列

    Deck_np = np.array(Reset(), dtype=object)

    return Deck_np


############################################################################################
#山札からNum枚カードを引く


def Draw(Deck,Num = 1,Del = 0):  #list

    Resalt = []

    if Del == 0:

        for i in range(Num):
            Resalt.append(Deck[0])
            del Deck[0]

        return Resalt

    else:

        for i in range(Num):
            Resalt.append(Deck[i])

        return Resalt


def Draw_np(Deck_np,Num = 1,Del = 0):  #Numpy配列

    Card_Data_list = []
    Deck_list = Deck_np.tolist()  #リストに変換

    if Del == 0:

        for i in range(Num):
            Card_Data_list.append(Deck_list[0])
            del Deck_list[0]

        Deck_np.resize(np.array(Deck_list, dtype=object).shape, refcheck = False)  #引数のNumpy配列をリサイズ

        Deck_np[:] = np.array(Deck_list, dtype=object)[:]
        Card_Data_np = np.array(Card_Data_list, dtype=object)


    else:

        for i in range(Num):
            Card_Data_list.append(Deck_list[i])

        Deck_np.resize(np.array(Deck_list, dtype=object).shape, refcheck = False)  #引数のNumpy配列をリサイズ

        Deck_np[:] = np.array(Deck_list, dtype=object)[:]  #Numpy配列に変換
        Card_Data_np = np.array(Card_Data_list, dtype=object)

    return Card_Data_np


############################################################################################
#山札からNum枚ランダムにカードを引く


def Draw_Random(Deck,Num = 1,Del = 0):  #list

    #random.seed()
    Resalt = []

    for i in range(Num):
        Count_Cards = len(Deck)
        Choose_Card = random.randint(0,Count_Cards-1)

        Resalt.append(Deck[Choose_Card])

        if Del == 0:
            del Deck[Choose_Card]

    return Resalt


def Draw_np_Random(Deck_np,Num = 1,Del = 0):  #Numpy配列

    Card_Data_list = []
    Deck_list = Deck_np.tolist()  #リストに変換

    for i in range(Num):
        Count_Cards = len(Deck_list)
        Choose_Card = random.randint(0,Count_Cards-1)

        Card_Data_list.append(Deck_list[Choose_Card])

        if Del == 0:  #山札から引いたカードを削除
            del Deck_list[Choose_Card]

    Deck_np.resize(np.array(Deck_list, dtype=object).shape, refcheck = False)  #引数のNumpy配列をリサイズ

    Deck_np[:] = np.array(Deck_list, dtype=object)[:]  #Numpy配列に変換
    Card_Data_np = np.array(Card_Data_list, dtype=object)

    return Card_Data_np


############################################################################################
#山札をシャッフル


def Shuffle(Deck,Overwrite_or_Create = 0):  #list

    if Overwrite_or_Create == 0:  #上書き ※破壊的メソッド
        random.shuffle(Deck)
        return

    elif Overwrite_or_Create == 1:  #新規作成
        Resalt = random.sample(Deck,len(Deck))
        return Resalt


def Shuffle_np(Deck,Overwrite_or_Create = 0):  #Numpy配列

    if Overwrite_or_Create == 0:  #上書き ※破壊的メソッド
        np.random.shuffle(Deck)
        return

    elif Overwrite_or_Create == 1:  #新規作成
        Resalt = np.random.permutation(Deck)
        return Resalt