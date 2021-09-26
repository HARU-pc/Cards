import numpy as np
import random

def Reset():

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

def Reset_np():
    Deck_np = np.array(Reset(), dtype=object)
    return Deck_np

def Draw(Deck,Num = 1,Del = 0):
    if Num == 1:
        if Del == 1:
            return [Deck[-1][0],Deck[-1][1],Deck[-1][2]]
        else:
            Card_Mark = Deck[-1][0]
            Card_Num = Deck[-1][1]
            Card_Name = Deck[-1][2]
            del Deck[-1]
            return [Card_Mark,Card_Num,Card_Name]

def Draw_Random(Deck,Num = 1,Del = 0):
    if Num == 1:
        Count_Cards = len(Deck)
        Choose_Card = random.randint(0,Count_Cards)
        if Del == 1:
            return [Deck[Choose_Card][0],Deck[Choose_Card][1],Deck[Choose_Card][2]]
        else:
            Card_Mark = Deck[Choose_Card][0]
            Card_Num = Deck[Choose_Card][1]
            Card_Name = Deck[Choose_Card][2]
            del Deck[Choose_Card]
            return [Card_Mark,Card_Num,Card_Name]

def Draw_np(Deck,Num = 1,Del = 0):
    if Num == 1:
        if Del == 1:
            return [Deck[-1][0],Deck[-1][1],Deck[-1][2]]
        else:
            Card_Mark = Deck[-1][0]
            Card_Num = Deck[-1][1]
            Card_Name = Deck[-1][2]
            Deck = np.delete(Deck, -1, 0)
            #return [Card_Mark,Card_Num,Card_Name]
            return [Deck,[Card_Mark,Card_Num,Card_Name]]

def Draw_np_Random(Deck,Num = 1,Del = 0):
    if Num == 1:
        Count_Cards = len(Deck)
        Choose_Card = random.randint(0,Count_Cards)
        if Del == 1:
            return [Deck[Choose_Card][0],Deck[Choose_Card][1],Deck[Choose_Card][2]]
        else:
            Card_Mark = Deck[Choose_Card][0]
            Card_Num = Deck[Choose_Card][1]
            Card_Name = Deck[Choose_Card][2]
            Deck = np.delete(Deck, Choose_Card, 0)
            #return [Card_Mark,Card_Num,Card_Name]
            return [Deck,[Card_Mark,Card_Num,Card_Name]]

