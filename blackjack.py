try:

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
        Game_data = {"money":0,"win":0,"lose":0,"draw":0,"game over":0,"lound":0}
        return Game_data

    def main_proc():

        Computer = 1
        Player = 0

        Win = 0
        Lose = 1
        Draw = 2

        Game_data = Get_Game_data()

        while True:

            print("BLACK JACK\nLet's enjoy\n\n")

            print('How much money do you have?\n$',end='')
            Game_data['money'] = Get_input_float()

            Game_data['lound'] = 0

            Win_or_Lose = 0

            while True:

                Game_data['lound'] += 1

                Computer_Cards = []
                Computer_Data = [0,0]

                Player_Cards = []
                Player_Data = [0,0]

                Deck = Cards.Reset()
                Cards.Shuffle(Deck)

                print(f'\n\nLOUND:{Game_data["lound"]}\n\nYour money:${Game_data["money"]}\n')

                print('Please bet.\n$',end='')
                Bet = Get_input_float()
                while Game_data['money'] < Bet or Bet <= 0:
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

                        Open_Card(Player_Cards,Player_Data[0],Player)

                        if Player_Data[0] > 21:
                            Player_Hit = 1

                    print(f'\nUPCARD:{Computer_Cards[0][0]}{Computer_Cards[0][2]}\nComputer has {len(Computer_Cards)} cards.')

                    Count += 1

                Open_Card(Player_Cards,Player_Data[0],Player)
                Open_Card(Computer_Cards,Computer_Data[0],Computer)

                if Player_Data[0] == 21 and len(Player_Cards) == 2:
                    print('Black Jack!!\nYou win!!!!')
                    Bet += int(Bet / 2)
                    Game_data['win'] += 1
                    Win_or_Lose = Win

                elif Player_Data[0] > 21:
                    print("YOU'RE BURSTED!!\n\nYou lose")
                    Game_data['lose'] += 1
                    Win_or_Lose = Lose
                    if Computer_Data[0] > 21:
                        print('Computer is BURSTED too!!')

                elif Computer_Data[0] > 21:
                    print('Computer is BURSTED!!\nYou win!!!!')
                    Game_data['win'] += 1
                    Win_or_Lose = Win

                elif Computer_Data[0] < Player_Data[0]:
                    print('You win!!!!')
                    Game_data['win'] += 1
                    Win_or_Lose = Win

                elif Player_Data[0] < Computer_Data[0]:
                    print('You lose')
                    Game_data['lose'] += 1
                    Win_or_Lose = Lose

                else:
                    print('Draw')
                    Game_data['draw'] += 1
                    Win_or_Lose = Draw

                if Win_or_Lose == Win:
                    Game_data['money'] += Bet
                elif Win_or_Lose == Lose:
                    Game_data['money'] -= Bet

                print(f'\nwin:{Game_data["win"]} lose:{Game_data["lose"]} Draw:{Game_data["draw"]}')

                print(f'Your Money:{Game_data["money"]}\n')

                if Game_data['money'] <= 0:
                    Game_data['game over'] += 1
                    print('GAME OVER\nDo you want to continue? [Y/n] ',end='')
                    Check_Retry = input()
                    while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Continue_or_Finish.lower()) == None:
                        print(f'ERROR:There is no {Check_Retry} in the choices.\nDo you want to continue? [Y/n] ',end='')
                        Check_Retry = input()

                    if re.search(r'[.*?y.*?|.*?0.*?]',Continue_or_Finish.lower()) == r'[y|1]':
                        Game_data['lound'] = 0
                        print('\n\nHow much money do you have?\n$',end='')
                        Game_data['money'] = Get_input_float()
                    else:
                        break

                else:
                    print('Do you want to continue? [Y/n] ',end='')
                    Continue_or_Finish = input()
                    while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Continue_or_Finish.lower()) == None:
                        print(f"ERROR:There is no '{Continue_or_Finish}' in the choices.\nDo you want to continue? [Y/n] ",end='')
                        Continue_or_Finish = input()
                    if Continue_or_Finish == 2 or re.search(r'[.*?n.*?|2]',Continue_or_Finish.lower()) != None:
                        break
            if Continue_or_Finish == 2 or re.search(r'[.*?n.*?|2]',Continue_or_Finish.lower()) != None:
                break

    main_proc()

    pass

except KeyboardInterrupt:
    pass