if __name__ == '__main__':
    print('Run main.py')

else:

    from module import Cards,Save_Data
    import re
    import os
    import sys


    NPC = 1
    PC = 0

    WIN = 0
    LOSE = 1
    DRAW = 2

    class Character_Data:

        def __init__(self,PC_or_NPC = 0) -> None:

            if PC_or_NPC == 0:

                self.money = 10000
                self.now_score = {'win':0,'lose':0,'draw':0}
                self.total_score = {'win':0,'lose':0,'draw':0}
                self.game_over = 0
                self.bet = None

            self.sum = 0
            self.ace = 0
            self.cards = []

            pass

        def Reset(self,PC_or_NPC = 0):

            if PC_or_NPC == 0:
                self.bet = None

            self.sum = 0
            self.ace = 0
            self.cards = []

        def Open_Card(self,PC_or_NPC = 0):

            if PC_or_NPC == 0:
                print("\n\nYour Cards")
            elif PC_or_NPC == 1:
                print("\n\nComputer's Cards")

            for i in list(range(0,len(self.cards))):
                print(f"CARDS{i + 1}:{self.cards[i][0]}{self.cards[i][2]}")
            print(f"TOTAL:{self.sum}")

            if PC_or_NPC == 0:
                print(f"\nYou have {len(self.cards)} cards.")
            elif PC_or_NPC == 1:
                print(f"\nComputer has {len(self.cards)} cards.")

        def Hit_Card(self,deck):

            self.cards.extend(Cards.Draw(deck))

            if self.cards[-1][1] == 1:
                self.sum += 11
                self.ace += 1
            else:
                if 10 < self.cards[-1][1]:
                    self.sum += 10
                else:
                    self.sum += self.cards[-1][1]


            while self.sum > 21 and self.ace > 0:
                self.sum -= 10
                self.ace -= 1

            return

        def Show_Status(self,PC_or_NPC = 0):
            if PC_or_NPC == 0:
                print('{0[0]}:{0[1]} {0[2]}:{0[3]} {0[4]}:{0[5]}\nYour money:${1}'.format([x for row in list(self.now_score.items()) for x in row],self.money))
            return

    class App:

        def __init__(self,User_Name=None,passwd=None) -> None:
            self.User_Name = User_Name
            self.passwd = passwd

            self.Index = 0

            os.chdir(os.path.dirname(os.path.abspath(__file__)))

            print("♥♦BLACK JACK♠♣\nLet's enjoy\n")

        def Create_new_user(self):

            self.Game_Data = Save_Data.Creat('blackjack',self.User_Name,self.passwd)
            self.Game_Data.deck = None
            self.Game_Data.lound = 0
            self.Game_Data.index = None
            self.Game_Data.PC_Data_for_save = Character_Data(PC)
            self.Game_Data.NPC_Data_for_save = Character_Data(NPC)

        def Load_Data(self):

            self.Game_Data = Save_Data.Load('blackjack',self.User_Name,self.passwd)

        def New_User_or_Load_Data(self):

            if os.path.isfile(f".data/blackjack/{self.User_Name}.bin"):
                self.Load_Data()
            else:
                self.Create_new_user()

            self.PC_Data = self.Game_Data.PC_Data_for_save
            self.NPC_Data = self.Game_Data.NPC_Data_for_save

        def Prepare_New_Game(self):

            self.Reset()

            self.Game_Data.lound = 0

            self.Game_Data.index = 2

        def Prepare_New_Lound(self):

            self.Reset()

            self.Game_Data.lound += 1
            self.Game_Data.index = 3

        def Bet(self):

            print(f'\n\nLOUND:{self.Game_Data.lound}\n\nYour money:${self.PC_Data.money}\n')

            while self.PC_Data.bet is None or type(self.PC_Data.bet) == str or self.PC_Data.money < self.PC_Data.bet or self.PC_Data.bet <= 0:

                try:
                    self.PC_Data.bet = float(input('Please bet:$').replace(',',''))  #コロンを削除
                except ValueError:  #文字列がある場合再度入力を求める
                    print("Please input numbers without letters")

            self.Game_Data.index = 4

        def Deal(self):

            for i in range(2):
                self.NPC_Data.Hit_Card(self.Game_Data.deck)
                self.PC_Data.Hit_Card(self.Game_Data.deck)

            self.Game_Data.index = 5

        def Play(self):

            self.PC_Data.Open_Card(PC)

            print(f'\nUPCARD:{self.NPC_Data.cards[0][0]}{self.NPC_Data.cards[0][2]}\nComputer has {len(self.NPC_Data.cards)} cards.')

            Player_Hit = 0
            while Player_Hit == 0 or self.NPC_Data.sum < 17:

                if self.NPC_Data.sum < 17:
                    print('\nComputer hit')
                    self.NPC_Data.Hit_Card(self.Game_Data.deck)

                else:
                    print('Computer stand')

                if Player_Hit == 0:
                    print("\nHIT:1 STAND(STAY):2")
                    Hit_or_Stand = input('Input field:')
                    while re.search(r'[.*?hit.*?|.*?sta.*?|1|2]',Hit_or_Stand.lower()) is None:
                        print("HIT:1 STAND(STAY):2")
                        Hit_or_Stand = input('Input field:')

                    if re.search(r'[.*?sta.*?|2]',Hit_or_Stand.lower()) != None:
                        Player_Hit = 1
                        continue

                    self.PC_Data.Hit_Card(self.Game_Data.deck)

                    self.PC_Data.Open_Card(PC)

                    if self.PC_Data.sum > 21:
                        Player_Hit = 1

                print(f'\nUPCARD:{self.NPC_Data.cards[0][0]}{self.NPC_Data.cards[0][2]}\nComputer has {len(self.NPC_Data.cards)} cards.')

            self.Game_Data.index = 6

        def Resalt(self):

            self.PC_Data.Open_Card(PC)
            self.NPC_Data.Open_Card(NPC)

            if self.PC_Data.sum == 21 and len(self.PC_Data.cards) == 2:
                print('Black Jack!!\nYou win!!!!')
                self.PC_Data.bet += int(self.PC_Data.bet / 2)
                self.PC_Data.now_score['win'] += 1
                self.PC_Data.total_score['win'] += 1
                Win_or_Lose = WIN

            elif self.PC_Data.sum > 21:
                print("YOU'RE BURSTED!!\n\nYou lose")
                self.PC_Data.now_score['lose'] += 1
                self.PC_Data.total_score['lose'] += 1
                Win_or_Lose = LOSE
                if self.NPC_Data.sum > 21:
                    print('Computer is BURSTED too!!')

            elif self.NPC_Data.sum > 21:
                print('Computer is BURSTED!!\nYou win!!!!')
                self.PC_Data.now_score['win'] += 1
                self.PC_Data.total_score['win'] += 1
                Win_or_Lose = WIN

            elif self.NPC_Data.sum < self.PC_Data.sum:
                print('You win!!!!')
                self.PC_Data.now_score['win'] += 1
                self.PC_Data.total_score['win'] += 1
                Win_or_Lose = WIN

            elif self.PC_Data.sum < self.NPC_Data.sum:
                print('You lose')
                self.PC_Data.now_score['lose'] += 1
                self.PC_Data.total_score['lose'] += 1
                Win_or_Lose = LOSE

            else:
                print('Draw')
                self.PC_Data.now_score['draw'] += 1
                self.PC_Data.total_score['draw'] += 1
                Win_or_Lose = DRAW

            if Win_or_Lose == WIN:
                self.PC_Data.money += self.PC_Data.bet
            elif Win_or_Lose == LOSE:
                self.PC_Data.money -= self.PC_Data.bet

            self.PC_Data.Show_Status(PC)

        def Reset(self):
            self.Game_Data.PC_Data_for_save.Reset(PC)
            self.Game_Data.NPC_Data_for_save.Reset(NPC)
            self.Game_Data.deck = Cards.Reset()
            Cards.Shuffle(self.Game_Data.deck)

        def Check_Game_Over(self):

            if self.PC_Data.money <= 0:
                self.PC_Data.game_over += 1
                self.PC_Data.money = float(10000 / int(10 ** self.PC_Data.game_over))
                if self.PC_Data.money < 100:
                    print('GAME OVER')
                    Check_Reset = input('Do you want to reset your data? [y/n] ')
                    while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Check_Reset.lower()) is None:
                        Check_Reset = input(f'ERROR:There is no {Check_Reset} in the choices.\nDo you want to reset your data? [y/n] ')
                    if re.search(r'[.*?y.*?|.*?1.*?]',Check_Reset.lower()) != None:
                        os.remove(f".data/blackjack/{self.User_Name}.bin")
                        self.Index = 0
                    else:
                        self.Game_Data.index = 1
                else:
                    self.Game_Data.index = 1

                    Check_Retry = input('GAME OVER\nDo you want to continue? [y/n] ')

                    while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Check_Retry.lower()) is None:
                        Check_Retry = input(f'ERROR:There is no {Check_Retry} in the choices.\nDo you want to continue? [y/n] ')
                    if re.search(r'[.*?y.*?|.*?1.*?]',Check_Retry.lower()) != None:
                        self.main()
                    else:
                        sys.exit()

        def Check_Continue(self):

            self.Game_Data.index = 2

            Continue_or_Finish = input('Do you want to continue? [y/n] ')
            while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Continue_or_Finish.lower()) is None:
                Continue_or_Finish = input(f"ERROR:There is no '{Continue_or_Finish}' in the choices.\nDo you want to continue? [Y/n] ")
            if Continue_or_Finish == 2 or re.search(r'[.*?n.*?|2]',Continue_or_Finish.lower()) != None:
                sys.exit()

        def main(self):

            while True:

                if self.Index == 0:
                    self.New_User_or_Load_Data()
                    self.Game_Data.index = 1 if self.Game_Data.index is None else self.Game_Data.index
                    self.Index = None
                    Save_Data.Save('blackjack',self.Game_Data)

                elif self.Game_Data.index == 1:

                    self.Prepare_New_Game()
                    Save_Data.Save('blackjack',self.Game_Data)

                elif self.Game_Data.index == 2:

                    self.Prepare_New_Lound()
                    Save_Data.Save('blackjack',self.Game_Data)

                elif self.Game_Data.index == 3:

                    self.Bet()
                    Save_Data.Save('blackjack',self.Game_Data)

                elif self.Game_Data.index == 4:

                    self.Deal()
                    Save_Data.Save('blackjack',self.Game_Data)

                elif self.Game_Data.index == 5:

                    self.Play()
                    Save_Data.Save('blackjack',self.Game_Data)

                elif self.Game_Data.index == 6:

                    Save_Data.Save('blackjack',self.Game_Data)

                    self.Resalt()

                    self.Check_Game_Over()

                    self.Check_Continue()