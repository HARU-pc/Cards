from my_module import Cards
import re
import os
import sys
import subprocess
import platform
import hashlib
import pickle

class Save_Data:
    def __init__(self,name,passwd) -> None:
        self.name = name
        self.passwd = passwd
        self.PC_Data_for_save = Character_Data(PC)
        self.NPC_Data_for_save = Character_Data(NPC)
class Character_Data:

    def __init__(self,pc_or_npc) -> None:

        if pc_or_npc == 0:

            self.money = 10000
            self.now_score = {'win':0,'lose':0,'draw':0}
            self.total_score = {'win':0,'lose':0,'draw':0}
            self.game_over = 0
            self.lound = 0
            self.bet = None

        self.sum = 0
        self.ace = 0
        self.cards = []

        pass

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

        self.cards.extend(Cards.Draw(Deck))

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

def Saving_Data():

    if not os.path.isdir(".data/blackjack"):
        os.makedirs(".data/blackjack")
        os.system('attrib +H /S /D .data')

    if Game_Data != None:
            with open(f".data/blackjack/{Game_Data.name}.pkl","wb") as f:
                pickle.dump(Game_Data, f)

def Create_new_user():

    global Game_Data

    while True:
        print('New user name:',end='')
        Name = input()

        if not os.path.isfile(f".data/blackjack/{Name}.pkl"):
            break
        else:
            print(f"The user `{Name}' already exists.")
            main()

    while True:
        print('New Password:',end='')
        Passwd = hashlib.sha256(input().encode()).hexdigest()
        print('Retype new Password:',end='')
        Passwd_Check = hashlib.sha256(input().encode()).hexdigest()
        if Passwd == Passwd_Check:
            break
        else:
            print('Sorry, passwords do not match.')
            print('Try again? [y/N]',end='')
            Check_Retry = input()
            while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Check_Retry.lower()) == None:
                print(f'ERROR:There is no {Check_Retry} in the choices.\nDo you want to continue? [Y/n] ',end='')
                Check_Retry = input()
            if re.search(r'[.*?y.*?|1]',Check_Retry.lower()) == None:
                sys.exit()

    Game_Data = Save_Data(Name,Passwd)
    Passwd = None
    Passwd_Check = None

def Load_Data():

    global Game_Data

    while True:
        print('User name:',end='')
        Name = input()

        if os.path.isfile(f".data/blackjack/{Name}.pkl"):
            break
        else:
            print(f"The user `{Name}' doesn't exists.")
            main()

    with open(f".data/blackjack/{Name}.pkl", "rb") as f:
        Game_Data = pickle.load(f)

    for i in range(3):
        print('Password:',end='')
        Passwd = hashlib.sha256(input().encode()).hexdigest()
        if Passwd == Game_Data.passwd:
            break
        elif i == 2:
            print('3 incorrect password attempts')
            Game_Data = None
            main()
        else:
            print('Sorry, try again.')



def Get_input_float():  #入力をfloatとして返す

    Input_phrase = input()

    while type(Input_phrase) == str:

        try:
            Input_phrase = float(Input_phrase.replace(',',''))  #コロンを削除
        except ValueError:  #文字列がある場合再度入力を求める
            print("Please input numbers without letters")
            Input_phrase = input()

    return Input_phrase

def New_User_or_Load_Data():

    global PC_Data,NPC_Data,Game_Data

    print('Create new user:1\nLoad save data:2')
    New_or_Load = input()
    while re.search(r'[.*?new.*?|.*?create.*?|.*?load.*?|1|2]',New_or_Load.lower()) == None:
        print(f'ERROR:There is no {New_or_Load} in the choices.\nCreate new Game:1\nLoad save data:2 ')
        New_or_Load = input()

    if re.search(r'[.*?new.*?|.*?create.*?|1]',New_or_Load.lower()) != None:
        Create_new_user()
    else:
        Load_Data()

    PC_Data = Game_Data.PC_Data_for_save
    NPC_Data = Game_Data.NPC_Data_for_save

def Prepare_New_Game():

    global PC_Data,NPC_Data

    print("BLACK JACK\nLet's enjoy\n\n")

    PC_Data.lound = 0
    NPC_Data.lound = 0

def Prepare_New_Lound():

    global PC_Data,NPC_Data,Deck

    PC_Data.lound += 1

    Deck = Cards.Reset()
    Cards.Shuffle(Deck)

    print(f'\n\nLOUND:{PC_Data.lound}\n\nYour money:${PC_Data.money}\n')

    print('Please bet.\n$',end='')
    PC_Data.bet = Get_input_float()
    while PC_Data.money < PC_Data.bet or PC_Data.bet <= 0:
        print('Please bet again.\n$',end='')
        PC_Data.bet = Get_input_float()

def Play():

    global PC_Data,NPC_Data,Deck

    for i in range(2):

        NPC_Data.Hit_Card()

        PC_Data.Hit_Card()

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
            Hit_or_Stand = input()
            while re.search(r'[.*?hit.*?|.*?sta.*?|1|2]',Hit_or_Stand.lower()) == None:
                print("HIT:1 STAND(STAY):2")
                Hit_or_Stand = input()

            if re.search(r'[.*?sta.*?|2]',Hit_or_Stand.lower()) != None:
                Player_Hit = 1
                continue

            PC_Data.Hit_Card()

            PC_Data.Open_Card(PC)

            if PC_Data.sum > 21:
                Player_Hit = 1

        print(f'\nUPCARD:{NPC_Data.cards[0][0]}{NPC_Data.cards[0][2]}\nComputer has {len(NPC_Data.cards)} cards.')

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

    global PC_Data,Check_Retry

    if PC_Data.money <= 0:
        PC_Data.game_over += 1
        PC_Data.money = 10000
        print('GAME OVER\nDo you want to continue? [y/n] ',end='')
        Check_Retry = input()
        while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Check_Retry.lower()) == None:
            print(f'ERROR:There is no {Check_Retry} in the choices.\nDo you want to continue? [Y/n] ',end='')
            Check_Retry = input()

        if re.search(r'[.*?y.*?|.*?1.*?]',Check_Retry.lower()) != None:
            main()
        else:
            sys.exit()

def Check_Continue():
    print('Do you want to continue? [y/n] ',end='')
    Continue_or_Finish = input()
    while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Continue_or_Finish.lower()) == None:
        print(f"ERROR:There is no '{Continue_or_Finish}' in the choices.\nDo you want to continue? [Y/n] ",end='')
        Continue_or_Finish = input()
    if Continue_or_Finish == 2 or re.search(r'[.*?n.*?|2]',Continue_or_Finish.lower()) != None:
        sys.exit()

def main():

    New_User_or_Load_Data()

    while True:

        if Check_Retry == None:
            Prepare_New_Game()

        while True:

            Prepare_New_Lound()

            Play()

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

        Check_Retry = None

        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        main()

    except KeyboardInterrupt:
        Saving_Data()
        pass

    except BaseException:
        Saving_Data()
        pass