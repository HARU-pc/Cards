from my_module import Cards
import re
import sys

def Get_input_float():  #入力をfloatとして返す

    Input_phrase = input()

    while type(Input_phrase) == str:

        try:
            Input_phrase = float(Input_phrase.replace(',',''))  #コロンを削除
        except ValueError:  #文字列がある場合再度入力を求める
            print("Please input numbers without letters")
            Input_phrase = input()

    return Input_phrase

def Open_Card(Cards,Sum,Player_or_Computer):

    if Player_or_Computer == 0:
        print("\n\nYour Cards")
    elif Player_or_Computer == 1:
        print("\n\nComputer's Cards")

    for i in list(range(0,len(Cards))):
        print(f"CARDS{i + 1}:{Cards[i][0]}{Cards[i][2]}")
    print(f"TOTAL:{Sum}")

    if Player_or_Computer == 0:
        print(f"\nYou have {len(Cards)} cards.")
    elif Player_or_Computer == 1:
        print(f"\nComputer has {len(Cards)} cards.")

def Hit_Card(Cards,Data):

        if Cards[-1][1] == 1:
            Data[0] += 11
            Data[1] += 1
        else:
            if 10 < Cards[-1][1]:
                Data[0] += 10
            else:
                Data[0] += Cards[-1][1]


        while Data[0] > 21 and Data[1] > 0:
            Data[0] -= 10
            Data[1] -= 1

        return

def Get_Game_data():

    global Game_data
    Game_data = {"money":0,"win":0,"lose":0,"draw":0,"game over":0,"lound":0}

    return

def Prepare_New_Game():

    global Game_data

    print("BLACK JACK\nLet's enjoy\n\n")

    print('How much money do you have?\n$',end='')
    Game_data['money'] = Get_input_float()

    Game_data['lound'] = 0

def Prepare_New_Lound():

    global Computer_Cards,Computer_Data,Player_Cards,Player_Data,Deck,Bet,Game_data

    Computer_Cards = []
    Computer_Data = [0,0]

    Player_Cards = []
    Player_Data = [0,0]

    Game_data['lound'] += 1

    Deck = Cards.Reset()
    Cards.Shuffle(Deck)

    print(f'\n\nLOUND:{Game_data["lound"]}\n\nYour money:${Game_data["money"]}\n')

    print('Please bet.\n$',end='')
    Bet = Get_input_float()
    while Game_data['money'] < Bet or Bet <= 0:
        print('Please bet again.\n$',end='')
        Bet = Get_input_float()

def Play():

    global Computer_Cards,Computer_Data,Player_Cards,Player_Data,Deck

    for i in range(2):

        Computer_Cards.extend(Cards.Draw(Deck))
        Hit_Card(Computer_Cards,Computer_Data)

        Player_Cards.extend(Cards.Draw(Deck))
        Hit_Card(Player_Cards,Player_Data)

    Open_Card(Player_Cards,Player_Data[0],PLAYER)

    print(f'\nUPCARD:{Computer_Cards[0][0]}{Computer_Cards[0][2]}\nComputer has {len(Computer_Cards)} cards.')

    Player_Hit = 0
    while Player_Hit == 0 or Computer_Data[0] < 17:

        if Computer_Data[0] < 17:
            print('\nComputer hit')
            Computer_Cards.extend(Cards.Draw(Deck))
            Hit_Card(Computer_Cards,Computer_Data)

        else:
            print('Computer stand')

        if Player_Hit == 0:
            print("\nHIT:1 STAND(STAY):2")
            Hit_or_Stand = input()
            while re.search(r'[.*?hit.*?|.*?sta.*?|1|2]',Hit_or_Stand.lower()) == None:
                print("HIT:1 STAND(STAY):2")
                Hit_or_Stand = input()

            if re.search(r'[.*?sta.*?|2]',Hit_or_Stand.lower()) != None:
                Player_Hit = 1
                continue

            Player_Cards.extend(Cards.Draw(Deck))
            Hit_Card(Player_Cards,Player_Data)

            Open_Card(Player_Cards,Player_Data[0],PLAYER)

            if Player_Data[0] > 21:
                Player_Hit = 1

        print(f'\nUPCARD:{Computer_Cards[0][0]}{Computer_Cards[0][2]}\nComputer has {len(Computer_Cards)} cards.')

def Resalt():

    global Computer_Cards,Computer_Data,Player_Cards,Player_Data,Bet,Game_data

    Open_Card(Player_Cards,Player_Data[0],PLAYER)
    Open_Card(Computer_Cards,Computer_Data[0],COMPUTER)

    if Player_Data[0] == 21 and len(Player_Cards) == 2:
        print('Black Jack!!\nYou win!!!!')
        Bet += int(Bet / 2)
        Game_data['win'] += 1
        Win_or_Lose = WIN

    elif Player_Data[0] > 21:
        print("YOU'RE BURSTED!!\n\nYou lose")
        Game_data['lose'] += 1
        Win_or_Lose = LOSE
        if Computer_Data[0] > 21:
            print('Computer is BURSTED too!!')

    elif Computer_Data[0] > 21:
        print('Computer is BURSTED!!\nYou win!!!!')
        Game_data['win'] += 1
        Win_or_Lose = WIN

    elif Computer_Data[0] < Player_Data[0]:
        print('You win!!!!')
        Game_data['win'] += 1
        Win_or_Lose = WIN

    elif Player_Data[0] < Computer_Data[0]:
        print('You lose')
        Game_data['lose'] += 1
        Win_or_Lose = LOSE

    else:
        print('Draw')
        Game_data['draw'] += 1
        Win_or_Lose = DRAW

    if Win_or_Lose == WIN:
        Game_data['money'] += Bet
    elif Win_or_Lose == LOSE:
        Game_data['money'] -= Bet

    print(f'\nwin:{Game_data["win"]} lose:{Game_data["lose"]} Draw:{Game_data["draw"]}')

    print(f'Your Money:{Game_data["money"]}\n')

def Check_Game_Over():

    global Game_data

    if Game_data['money'] <= 0:
        Game_data['game over'] += 1
        print('GAME OVER\nDo you want to continue? [Y/n] ',end='')
        Check_Retry = input()
        while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Check_Retry.lower()) == None:
            print(f'ERROR:There is no {Check_Retry} in the choices.\nDo you want to continue? [Y/n] ',end='')
            Check_Retry = input()

        if re.search(r'[.*?y.*?|.*?1.*?]',Check_Retry.lower()) != None:
            main()
        else:
            sys.exi()

def Check_Continue():
    print('Do you want to continue? [Y/n] ',end='')
    Continue_or_Finish = input()
    while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Continue_or_Finish.lower()) == None:
        print(f"ERROR:There is no '{Continue_or_Finish}' in the choices.\nDo you want to continue? [Y/n] ",end='')
        Continue_or_Finish = input()
    if Continue_or_Finish == 2 or re.search(r'[.*?n.*?|2]',Continue_or_Finish.lower()) != None:
        sys.exi()

def main():

    Get_Game_data()

    while True:

        Prepare_New_Game()

        while True:

            Prepare_New_Lound()

            Play()

            Resalt()

            Check_Game_Over()

            Check_Continue()

if __name__ == '__main__':

    try:

        COMPUTER = 1
        PLAYER = 0

        WIN = 0
        LOSE = 1
        DRAW = 2

        Game_data = None
        Computer_Cards = None
        Computer_Data = None
        Player_Cards = None
        Player_Data = None
        Deck = None
        Bet = None

        main()

    except KeyboardInterrupt:
        pass
