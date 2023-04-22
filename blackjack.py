from module import Cards,Save_Data
import re
import os
import sys


NPC = 1
PC = 0

WIN = 0
LOSE = 1
DRAW = 2

'''
class Save_Data:
    def __init__(self,name=None,passwd=None) -> None:
        self.name = name
        self.passwd = passwd
        self.deck = None
        self.lound = 0
        self.index = None
        self.PC_Data_for_save = Character_Data(PC)
        self.NPC_Data_for_save = Character_Data(NPC)

    def Reset(self):
        self.PC_Data_for_save.Reset(PC)
        self.NPC_Data_for_save.Reset(NPC)
        self.deck = Cards.Reset()
        Cards.Shuffle(self.deck)

    def Save(self):

        if not os.path.isdir(".data/blackjack"):
            os.makedirs(".data/blackjack")

        if platform.system() == 'Windows':
            subprocess.Popen(['attrib','+H','.data'],shell=True)

        if self.name != None:
                with open(f".data/blackjack/{self.name}.bin","wb") as f:
                    f.write(Aes.encrypt(dill.dumps(self), self.passwd))

    def Load():

        while True:
            Name = input('\nUser name:')

            if os.path.isfile(f".data/blackjack/{Name}.bin"):
                break
            else:
                print(f"The user `{Name}' doesn't exists.")
                BlackJack.main()

        for i in range(3):
            Passwd = hashlib.sha256(getpass(prompt='Password:',stream=sys.stderr).encode()).hexdigest()

            with open(f".data/blackjack/{Name}.bin", "rb") as f:
                try:
                    Data = dill.loads(Aes.decrypt(f.read(), Passwd))
                except dill.UnpicklingError:
                    Data = 1
                    pass

            if Data != 1 and Data.passwd == Passwd:
                break
            elif i == 2:
                print('3 incorrect password attempts')
                Data = None
                BlackJack.main()
            else:
                print('Sorry, try again.')

        return Data

    def Creat():
        while True:
            Name = input('\nNew user name:')

            if not os.path.isfile(f".data/blackjack/{Name}.bin"):
                break
            else:
                print(f"The user `{Name}' already exists.")
                BlackJack.main()

        while True:
            Passwd = hashlib.sha256(getpass(prompt='New Password:',stream=sys.stderr).encode()).hexdigest()
            Passwd_Check = hashlib.sha256(getpass(prompt='Retype new Password:',stream=sys.stderr).encode()).hexdigest()

            if Passwd == Passwd_Check:
                break
            else:
                print('Sorry, passwords do not match.')
                Check_Retry = input('Try again? [y/N]')
                while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Check_Retry.lower()) == None:
                    Check_Retry = input(f'ERROR:There is no {Check_Retry} in the choices.\nDo you want to continue? [Y/n] ')
                if re.search(r'[.*?y.*?|1]',Check_Retry.lower()) == None:
                    sys.exit()

        Data = Save_Data(Name, Passwd)
        Passwd = None
        Passwd_Check = None

        return Data
'''
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

        self.Game_Data = Save_Data.Data.Creat('blackjack',self.User_Name,self.passwd)
        self.Game_Data.deck = None
        self.Game_Data.lound = 0
        self.Game_Data.index = None
        self.Game_Data.PC_Data_for_save = Character_Data(PC)
        self.Game_Data.NPC_Data_for_save = Character_Data(NPC)

    def Load_Data(self):

        self.Game_Data = Save_Data.Data.Load('blackjack',self.User_Name,self.passwd)

    def New_User_or_Load_Data(self):

        if os.path.isfile(f".data/blackjack/{self.User_Name}.bin"):
            self.Load_Data()
        else:
            self.Create_new_user()

        self.PC_Data = self.Game_Data.PC_Data_for_save
        self.NPC_Data = self.Game_Data.NPC_Data_for_save

    def Prepare_New_Game(self):

        self.Game_Data.Reset()

        self.Game_Data.lound = 0

        self.Game_Data.index = 2

    def Prepare_New_Lound(self):

        self.Game_Data.Reset()

        self.Game_Data.lound += 1
        self.Game_Data.index = 3

    def Bet(self):

        print(f'\n\nLOUND:{self.Game_Data.lound}\n\nYour money:${self.PC_Data.money}\n')

        while self.PC_Data.bet == None or type(self.PC_Data.bet) == str or self.PC_Data.money < self.PC_Data.bet or self.PC_Data.bet <= 0:

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
                while re.search(r'[.*?hit.*?|.*?sta.*?|1|2]',Hit_or_Stand.lower()) == None:
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

    def Check_Game_Over(self):

        if self.PC_Data.money <= 0:
            self.PC_Data.game_over += 1
            self.PC_Data.money = float(10000 / int(10 ** self.PC_Data.game_over))
            if self.PC_Data.money < 100:
                print('You died.')
                self.Game_Data = None
                self.Index = 0
            else:
                self.Game_Data.index = 1

            Check_Retry = input('GAME OVER\nDo you want to continue? [y/n] ')

            while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Check_Retry.lower()) == None:
                Check_Retry = input(f'ERROR:There is no {Check_Retry} in the choices.\nDo you want to continue? [Y/n] ')
            if re.search(r'[.*?y.*?|.*?1.*?]',Check_Retry.lower()) != None:
                self.main()
            else:
                sys.exit()

    def Check_Continue(self):

        self.Game_Data.index = 2

        Continue_or_Finish = input('Do you want to continue? [y/n] ')
        while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Continue_or_Finish.lower()) == None:
            Continue_or_Finish = input(f"ERROR:There is no '{Continue_or_Finish}' in the choices.\nDo you want to continue? [Y/n] ")
        if Continue_or_Finish == 2 or re.search(r'[.*?n.*?|2]',Continue_or_Finish.lower()) != None:
            sys.exit()

    def main(self):

        while True:

            if self.Index == 0:
                self.New_User_or_Load_Data()
                self.Game_Data.index = 1 if self.Game_Data.index == None else self.Game_Data.index
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