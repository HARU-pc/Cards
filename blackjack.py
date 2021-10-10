from my_module import Cards
import re


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

    if Player_or_Computer == 0:
        print(f"\nYou have {len(Cards)} cards.")
    elif Player_or_Computer == 1:
        print(f"\nComputer has {len(Cards)} cards.")

    print(f"TOTAL:{Sum}")


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


try:
    Computer = 1
    Player = 0

    Win = 0
    Lose = 1
    Draw = 2
    while True:

        Num = 0
        Card = 0
        Money = 0

        print("BLACK JACK\nLet's enjoy\n\n")

        print('How much money do you have?\n$',end='')
        Money = Get_input_float()

        Loop = 0
        Lound = 0

        Player_Win_counter = 0
        Computer_Win_counter = 0
        Draw_counter = 0

        Win_or_Lose = 0

        while True:

            Lound = Lound + 1

            Computer_Cards = []
            Computer_Data = [0,0]

            Player_Cards = []
            Player_Data = [0,0]

            Deck = Cards.Reset()
            Cards.Shuffle(Deck)

            print(f'LOUND:{Lound}\n\nYour money:${Money}\n')

            print('Please bet.\n$',end='')
            Bet = Get_input_float()
            while Bet > Money or Bet <= 0:
                print('Please bet again.\n$',end='')
                Bet = Get_input_float()

            Count = 0

            for i in range(2):

                Computer_Cards.extend(Cards.Draw(Deck))
                Hit_Card(Computer_Cards,Computer_Data)

                Player_Cards.extend(Cards.Draw(Deck))
                Hit_Card(Player_Cards,Player_Data)

                Count += 1

            Open_Card(Player_Cards,Player_Data[0],Player)

            print(f'UPCARD:{Computer_Cards[0][0]}{Computer_Cards[0][2]}\nComputer has {len(Computer_Cards)} cards.')

            Player_Hit = 0
            while Player_Hit == 0 or Computer_Data[0] < 17:

                if Computer_Data[0] < 17:

                    print('\nComputer hit')
                    Computer_Cards.extend(Cards.Draw(Deck))
                    Hit_Card(Computer_Cards,Computer_Data)

                else:
                    print('Computer stand')
                    print(f'UPCARD:{Computer_Cards[0][0]}{Computer_Cards[0][2]}\nComputer has {len(Computer_Cards)} cards.')

                if Player_Hit == 0:
                    print("\nHIT:1 STAND(STAY):2")
                    Hit_or_Stand = Get_input_float()
                    while Hit_or_Stand != 1 and Hit_or_Stand != 2:
                        print("HIT:1 STAND(STAY):2  !! 1 OR 2 !! ")
                        Hit_or_Stand = Get_input_float()

                    if Hit_or_Stand == 2:
                        Player_Hit = 1
                        continue

                    Player_Cards.extend(Cards.Draw(Deck))
                    Hit_Card(Player_Cards,Player_Data)

                    Open_Card(Player_Cards,Player_Data[0],Player)

                    if Player_Data[0] > 21:
                        print("YOU'RE BURSTED!!\n\nYou lose\n")
                        Player_Hit = 1

                Count += 1

                print(f'UPCARD:{Computer_Cards[0][0]}{Computer_Cards[0][2]}\nComputer has {len(Computer_Cards)} cards.')

            Open_Card(Player_Cards,Player_Data[0],Player)
            Open_Card(Computer_Cards,Computer_Data[0],Computer)

            if Player_Data[0] > 21:
                Computer_Win_counter += 1
                Win_or_Lose = Lose
                if Computer_Data[0] > 21:
                    print('Computer is BURSTED too!!')

            elif Computer_Data[0] > 21:
                print('Computer is BURSTED!!\nYou win!!!!')
                Player_Win_counter += 1
                Win_or_Lose = Win

            elif Computer_Data[0] < Player_Data[0]:
                print('You win!!!!')
                Player_Win_counter += 1
                Win_or_Lose = Win

            elif Player_Data[0] < Computer_Data[0]:
                print('You lose')
                Computer_Win_counter += 1
                Win_or_Lose = Lose

            else:
                print('Draw')
                Win_or_Lose = Draw

            if Player_Data[0] == 21 and len(Player_Cards) == 2:
                Bet += int(Bet / 2)

            if Win_or_Lose == Win:
                Money += Bet
            elif Win_or_Lose == Lose:
                Money -= Bet


            print(f'Your Money:{Money}\n')

            if Money <= 0:
                print('GAME OVER\nWill you retry?  Yes:1 No:2')
                Check_Retry = input()
                while Check_Retry != 1|2 and Check_Retry.lower() != r'.*yes.*|.*no.*':
                    print(f'ERROR:There is no {Check_Retry} in the choices.\nWill you retry?  Yes:1 No:2')
                    Check_Retry = input()

                if Check_Retry == 1 or Check_Retry.lower() == r'.*yes.*':
                    Lound = 0
                    print('\n\nHow much money do you have?\n$',end='')
                    Money = Get_input_float()
                else:
                    break
            
            else:
                print('Continue:1 Finish:2')
                Continue_or_Finish = input()
                while re.search(r'[1|2]',Continue_or_Finish.lower()) == None and re.search(r'[.*?yes.*?|.*?no.*?|.*?continue.*?|.*?fin.*?]',Continue_or_Finish.lower()) == None:
                    print(f"ERROR:There is no '{Continue_or_Finish}' in the choices.\nContinue:1 Finish:2")
                    Continue_or_Finish = input()
                if Continue_or_Finish == 2 or re.search(r'[.*?no.*?|.*?fin.*?]',Continue_or_Finish.lower()) != None:
                    break     
        if Continue_or_Finish == 2 or re.search(r'[.*?no.*?|.*?fin.*?]',Continue_or_Finish.lower()) != None:
            break
        pass

except KeyboardInterrupt:
    pass