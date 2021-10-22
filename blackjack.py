from module import Cards,Aes
import re
import os
import sys
import subprocess
import platform
import hashlib
import pickle
from getpass import getpass

class Save_Data:
    def __init__(self,name,passwd) -> None:
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

        if self != None:
                with open(f".data/blackjack/{self.name}.bin","wb") as f:
                    #pickle.dump(self, f)
                    f.write(Aes.encrypt(pickle.dumps(self), self.passwd))

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

    def Hit_Card(self):

        global Game_Data

        self.cards.extend(Cards.Draw(Game_Data.deck))

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

def Create_new_user():

    global Game_Data

    while True:
        Name = input('\nNew user name:')

        if not os.path.isfile(f".data/blackjack/{Name}.bin"):
            break
        else:
            print(f"The user `{Name}' already exists.")
            main()

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

    Game_Data = Save_Data(Name,Passwd)
    Passwd = None
    Passwd_Check = None

def Load_Data():

    global Game_Data

    while True:
        Name = input('\nUser name:')

        if os.path.isfile(f".data/blackjack/{Name}.bin"):
            break
        else:
            print(f"The user `{Name}' doesn't exists.")
            main()

    for i in range(3):
        Passwd = hashlib.sha256(getpass(prompt='Password:',stream=sys.stderr).encode()).hexdigest()

        if i == 0:
            with open(f".data/blackjack/{Name}.bin", "rb") as f:
                Game_Data = pickle.loads(Aes.decrypt(f.read(), Passwd))

        if Passwd == Game_Data.passwd:
            break
        elif i == 2:
            print('3 incorrect password attempts')
            Game_Data = None
            main()
        else:
            print('Sorry, try again.')

def New_User_or_Load_Data():

    global PC_Data,NPC_Data

    print('\nCreate new user:1\nLoad save data:2')
    New_or_Load = input('Input field:')
    while re.search(r'[.*?new.*?|.*?create.*?|.*?load.*?|1|2]',New_or_Load.lower()) == None:
        print(f'\nERROR:There is no {New_or_Load} in the choices.\nCreate new Game:1\nLoad save data:2 ')
        New_or_Load = input('Input field:')

    if re.search(r'[.*?new.*?|.*?create.*?|1]',New_or_Load.lower()) != None:
        Create_new_user()
    elif re.search(r'[.*?load.*?|2]',New_or_Load.lower()) != None:
        Load_Data()

    PC_Data = Game_Data.PC_Data_for_save
    NPC_Data = Game_Data.NPC_Data_for_save

def Prepare_New_Game():

    global Game_Data

    Game_Data.lound = 0

    Game_Data.index = 2

def Prepare_New_Lound():

    global PC_Data,Game_Data

    Game_Data.Reset()

    Game_Data.lound += 1
    Game_Data.index = 3

def Bet():

    global PC_Data,Game_Data

    print(f'\n\nLOUND:{Game_Data.lound}\n\nYour money:${PC_Data.money}\n')

    while PC_Data.bet == None or type(PC_Data.bet) == str or PC_Data.money < PC_Data.bet or PC_Data.bet <= 0:

        try:
            PC_Data.bet = float(input('Please bet:$').replace(',',''))  #コロンを削除
        except ValueError:  #文字列がある場合再度入力を求める
            print("Please input numbers without letters")

    Game_Data.index = 4

def Deal():

    global PC_Data,NPC_Data,Game_Data

    for i in range(2):
        NPC_Data.Hit_Card()
        PC_Data.Hit_Card()

    Game_Data.index = 5

def Play():

    global PC_Data,NPC_Data,Game_Data

    PC_Data.Open_Card(PC)

    print(f'\nUPCARD:{NPC_Data.cards[0][0]}{NPC_Data.cards[0][2]}\nComputer has {len(NPC_Data.cards)} cards.')

    Player_Hit = 0
    while Player_Hit == 0 or NPC_Data.sum < 17:

        if NPC_Data.sum < 17:
            print('\nComputer hit')
            NPC_Data.Hit_Card()

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

            PC_Data.Hit_Card()

            PC_Data.Open_Card(PC)

            if PC_Data.sum > 21:
                Player_Hit = 1

        print(f'\nUPCARD:{NPC_Data.cards[0][0]}{NPC_Data.cards[0][2]}\nComputer has {len(NPC_Data.cards)} cards.')

    Game_Data.index = 6

def Resalt():

    global PC_Data,NPC_Data

    PC_Data.Open_Card(PC)
    NPC_Data.Open_Card(NPC)

    if PC_Data.sum == 21 and len(PC_Data.cards) == 2:
        print('Black Jack!!\nYou win!!!!')
        PC_Data.bet += int(PC_Data.bet / 2)
        PC_Data.now_score['win'] += 1
        PC_Data.total_score['win'] += 1
        Win_or_Lose = WIN

    elif PC_Data.sum > 21:
        print("YOU'RE BURSTED!!\n\nYou lose")
        PC_Data.now_score['lose'] += 1
        PC_Data.total_score['lose'] += 1
        Win_or_Lose = LOSE
        if NPC_Data.sum > 21:
            print('Computer is BURSTED too!!')

    elif NPC_Data.sum > 21:
        print('Computer is BURSTED!!\nYou win!!!!')
        PC_Data.now_score['win'] += 1
        PC_Data.total_score['win'] += 1
        Win_or_Lose = WIN

    elif NPC_Data.sum < PC_Data.sum:
        print('You win!!!!')
        PC_Data.now_score['win'] += 1
        PC_Data.total_score['win'] += 1
        Win_or_Lose = WIN

    elif PC_Data.sum < NPC_Data.sum:
        print('You lose')
        PC_Data.now_score['lose'] += 1
        PC_Data.total_score['lose'] += 1
        Win_or_Lose = LOSE

    else:
        print('Draw')
        PC_Data.now_score['draw'] += 1
        PC_Data.total_score['draw'] += 1
        Win_or_Lose = DRAW

    if Win_or_Lose == WIN:
        PC_Data.money += PC_Data.bet
    elif Win_or_Lose == LOSE:
        PC_Data.money -= PC_Data.bet

    PC_Data.Show_Status(PC)

def Check_Game_Over():

    global PC_Data,Game_Data,Index

    if PC_Data.money <= 0:
        PC_Data.game_over += 1
        PC_Data.money = float(10000 / int(10 ** PC_Data.game_over))
        if PC_Data.money < 100:
            print('You died.')
            Game_Data = None
            Index = 0
        else:
            Game_Data.index = 1

        Check_Retry = input('GAME OVER\nDo you want to continue? [y/n] ')

        while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Check_Retry.lower()) == None:
            Check_Retry = input(f'ERROR:There is no {Check_Retry} in the choices.\nDo you want to continue? [Y/n] ')
        if re.search(r'[.*?y.*?|.*?1.*?]',Check_Retry.lower()) != None:
            main()
        else:
            sys.exit()

def Check_Continue():

    Game_Data.index = 2

    Continue_or_Finish = input('Do you want to continue? [y/n] ')
    while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Continue_or_Finish.lower()) == None:
        Continue_or_Finish = input(f"ERROR:There is no '{Continue_or_Finish}' in the choices.\nDo you want to continue? [Y/n] ")
    if Continue_or_Finish == 2 or re.search(r'[.*?n.*?|2]',Continue_or_Finish.lower()) != None:
        sys.exit()

def main():

    global Index

    while True:

        if Index == 0:
            New_User_or_Load_Data()
            Game_Data.index = 1 if Game_Data.index == None else Game_Data.index
            Index = None

        elif Game_Data.index == 1:
            Game_Data.Reset()
            Prepare_New_Game()

        elif Game_Data.index == 2:

            Prepare_New_Lound()

        elif Game_Data.index == 3:

            Bet()

        elif Game_Data.index == 4:

            Deal()

        elif Game_Data.index == 5:

            Play()

        elif Game_Data.index == 6:

            Resalt()

            Check_Game_Over()

            Check_Continue()

if __name__ == '__main__':

    try:
        NPC = 1
        PC = 0
        WIN = 0
        LOSE = 1
        DRAW = 2

        PC_Data = None
        NPC_Data = None
        Game_Data = None
        Index = 0

        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        print("♥♦BLACK JACK♠♣\nLet's enjoy\n")

        main()

    except KeyboardInterrupt:
        Game_Data.Save()
        pass

    except BaseException:
        Game_Data.Save()
        pass