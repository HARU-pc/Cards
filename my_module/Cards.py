import numpy as np
import random




def Reset():  #山札を作成

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



def Reset_np():  #Numpyで山札を作成

    Deck_np = np.array(Reset(), dtype=object)

    return Deck_np



def Draw(Deck,Num = 1,Del = 0):  #Num枚カードを引く

    Resalt = []

    if Del == 0:

        for i in range(Num):
            Resalt.append(Deck[-1])
            del Deck[-1]

        return Resalt

    else:

        for i in range(Num):
            i += 1
            Resalt.append(Deck[-i])

        return Resalt


def Draw_Random(Deck,Num = 1,Del = 0):  #Num枚ランダムにカードを引く

    #random.seed()
    Resalt = []

    for i in range(Num):
        Count_Cards = len(Deck)
        Choose_Card = random.randint(0,Count_Cards-1)

        if Del == 0:
            del Deck[Choose_Card]
        Resalt.append(Deck[Choose_Card])

    return Resalt


def Draw_np(Deck_np,Num = 1,Del = 0):  #Numpy配列の山札からNum枚カードを引く

    Card_Data_list = []
    Deck_list = Deck_np.tolist()

    if Del == 0:

        for i in range(Num):
            Card_Data_list.append(Deck_list[-1])
            del Deck_list[-1]
        Deck_np = np.array(Deck_list, dtype=object)
        Card_Data_np = np.array(Card_Data_list, dtype=object)
        Resalt_np = np.array([Deck_np,Card_Data_np], dtype=object)


    else:

        for i in range(Num):
            i += 1
            Card_Data_list.append(Deck_list[-i])
        Deck_np = np.array(Deck_list, dtype=object)
        Card_Data_np = np.array(Card_Data_list, dtype=object)
        Resalt_np = np.array([Deck_np,Card_Data_np], dtype=object)

    return Resalt_np


def Draw_np_Random(Deck_np,Num = 1,Del = 0):  #Numpy配列の山札からNum枚ランダムにカードを引く

    Card_Data_list = []
    Deck_list = Deck_np.tolist()

    for i in range(Num):
        Count_Cards = len(Deck_list)
        Choose_Card = random.randint(0,Count_Cards-1)

        if Del == 0:
            del Deck_list[Choose_Card]
        Card_Data_list.append(Deck_list[Choose_Card])

    Deck_np = np.array(Deck_list, dtype=object)
    Card_Data_np = np.array(Card_Data_list, dtype=object)
    Resalt_np = np.array([Deck_np,Card_Data_np], dtype=object)

    return Resalt_np

def Shuffle():

    return


def Shuffle_np(Deck,Overwrite_or_Create = 0):  #山札をシャッフル

    if Overwrite_or_Create == 0:  #上書き※破壊的メソッド
        np.random.shuffle(Deck)
        return

    elif Overwrite_or_Create == 1:  #新規作成
        Resalt = np.random.permutation(Deck)
        return Resalt