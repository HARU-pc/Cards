from my_module import Cards


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
        print("\n\nOpen you're cards.")
    elif Player_or_Computer == 1:
        print("\n\nOpen computer's cards.")

    for i in list(range(0,len(Cards))):
        print(f"CARDS:{Cards[i][0]}{Cards[i][2]}")

    if Player_or_Computer == 0:
        print(f"\nYou have {len(Cards)} cards.")
    elif Player_or_Computer == 1:
        print(f"\nComputer has {len(Cards)} cards.")

    print(f"TOTAL:{Sum}")


def Hit_Card(Cards,Ace,Sum):

        if Cards[-1][1] == 1:
            Ace += 1
        Sum += Cards[-1][1]

        while Sum > 21 and Ace > 0:
            Sum -= 10
            Ace -= 1

        return


try:
    while True:

        Num = 0
        Card = 0
        Money = 0

        print('BLACK JACK\nPlease enjoy\n\n')

        print('How much?\n$ ',end='')
        Money = Get_input_float()

        Loop = 0
        Lound = 0

        Player_Win = 0
        Computer_Win = 0
        Draw = 0

        Win_or_Lose = 0

        while True:

            Lound = Lound + 1

            Computer = 1
            Computer_Sum = 0
            Computer_Ace = 0
            Computer_Cards = []

            Player = 0
            Player_Sum = 0
            Player_Ace = 0
            Player_Cards = []

            Deck = Cards.Reset()
            Cards.Shuffle(Deck)

            print(f'LOUND:{Lound}\n\n$:{Money}\n')

            print('Please bet.\n$ ',end='')
            Bet = Get_input_float()
            while Bet > Money or Bet <= 0:
                print('Please bet again.\n$',end='')
                Bet = Get_input_float()

            Count = 0

            for i in range(2):

                Computer_Cards.extend(Cards.Draw(Deck))
                Computer_Sum += Computer_Cards[-1][1]
                Hit_Card(Computer_Cards,Computer_Ace,Computer_Sum)

                Player_Cards.extend(Cards.Draw(Deck))
                Player_Sum += Player_Cards[-1][1]
                Hit_Card(Player_Cards,Player_Ace,Player_Sum)

                Count += 1

            Open_Card(Player_Cards,Player_Sum,Player)

            print(f'UPCARD:{Computer_Cards[0][0]}{Computer_Cards[0][2]}\nComputer has {len(Computer_Cards)} cards.')

            Player_Hit = 0
            while Player_Hit == 0 or Computer_Sum < 17:

                if Computer_Sum < 17:

                    print('\nCOM HIT')
                    Computer_Cards.extend(Cards.Draw(Deck))
                    Computer_Sum += Computer_Cards[-1][1]
                    Hit_Card(Computer_Cards,Computer_Ace,Computer_Sum)

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
                    Player_Sum += Player_Cards[-1][1]
                    Hit_Card(Player_Cards,Player_Ace,Player_Sum)

                    Open_Card(Player_Cards,Player_Sum,Player)

                    if Player_Sum > 21:
                        print("YOU'RE BURSTED!!\n\nYOU LOSE!!\n")
                        Player_Hit = 1

                Count += 1

                print(f'UPCARD:{Computer_Cards[0][0]}{Computer_Cards[0][2]}\nComputer has {len(Computer_Cards)} cards.')


            pass

except KeyboardInterrupt:
    pass