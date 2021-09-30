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

def Draw(Deck,Num = 1,Del = 0):  #Num枚(デフォルトは1)カードを引く
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

def Draw_Random(Deck,Num = 1,Del = 0):  #Num枚(デフォルトは1それ以外は未実装)ランダムにカードを引く
    #random.seed()
    Resalt = []
    for i in range(Num):
        Count_Cards = len(Deck)
        Choose_Card = random.randint(0,Count_Cards-1)
        if Del == 0:
            del Deck[Choose_Card]
        Resalt.append(Deck[Choose_Card])
    return Resalt

def Draw_np(Deck,Num = 1,Del = 0):  #Numpy配列の山札からNum枚(デフォルトは1それ以外は未実装)カードを引く
    if Num == 1:
        if Del == 0:
            Card_Data = Deck[-1]
            Deck = np.delete(Deck, -1, 0)
            return [Deck,Card_Data]
    else:
        print("Unimplemented")
        return

def Draw_np_Random(Deck,Num = 1,Del = 0):  #Numpy配列の山札からNum枚(デフォルトは1それ以外は未実装)ランダムにカードを引く
    if Num == 1:
        Count_Cards = len(Deck)
        Choose_Card = random.randint(0,Count_Cards-1)
        Card_Data = Deck[Choose_Card]
        Deck = np.delete(Deck, Choose_Card, 0)
        return [Deck,Card_Data]
    else:
        print("Unimplemented")
        return


