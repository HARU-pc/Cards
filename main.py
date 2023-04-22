from module import Save_Data
import re
import os
from getpass import getpass
import blackjack


class Main:

    def __init__(self) -> None:

        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        print("♥♦Welcome!!♠♣\nLet's enjoy\n")

    def Create_new_user(self):

        self.Game_Data = Save_Data.Data.Creat(Game_Name)
        if self.Game_Data == None:
            self.New_User_or_Load_Data()
        else:
            Save_Data.Save(Game_Name,self.Game_Data)
            self.Select_Game()

    def Load_Data(self):

        self.Game_Data = Save_Data.Data.Load(Game_Name)
        if self.Game_Data == None:
            self.New_User_or_Load_Data()
        else:
            self.Select_Game()

    def New_User_or_Load_Data(self):

        print('\nCreate new user:1\nLoad save data:2')
        New_or_Load = input('Input field:')
        while re.search(r'[.*?new.*?|.*?create.*?|.*?load.*?|1|2]',New_or_Load.lower()) == None:
            print(f'\nERROR:There is no {New_or_Load} in the choices.\nCreate new Game:1\nLoad save data:2 ')
            New_or_Load = input('Input field:')

        if re.search(r'[.*?new.*?|.*?create.*?|1]',New_or_Load.lower()) != None:
            self.Create_new_user()
        elif re.search(r'[.*?load.*?|2]',New_or_Load.lower()) != None:
            self.Load_Data()

    def Select_Game(self):

        Games = ["Blackjack"]
        Game_List_Number = 0
        print("\nGame List\n")

        for Game_List in Games:
            Game_List_Number += 1
            print(Game_List_Number,":",Game_List,"\n")

        Chosen_Game = input("\nWhich game do you like?  ")

        while Chosen_Game != '1':
            print("Please select a game by number.")
            Chosen_Game = input("\nWhich game do you like?  ")

        if Chosen_Game == '1':
            self.Game_Data.Play_Now = 'blackjack'
            self.Playing = blackjack.App(self.Game_Data.name,self.Game_Data.passwd)
            self.Playing.main()
try:
    Game_Name = 'Home'
    Home = Main()
    Home.New_User_or_Load_Data()
    Home.Select_Game()

except (KeyboardInterrupt, BaseException):

    Save_Data.Save(Game_Name.Home.Game_Data)
    Save_Data.Save(Home.Game_Data.Play_Now,Home.Playing.Game_Data)

    print("\n\nThank you for playing!!")
    pass
