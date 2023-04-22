from module import Aes
import re
import os
import sys
import subprocess
import platform
import hashlib
import dill
from getpass import getpass


class Data:
    def __init__(self,name=None,passwd=None) -> None:
        self.name = name
        self.passwd = passwd
        self.Play_Now = None

    def Save(Game_Name,Data):

        if not os.path.isdir(f".data/{Game_Name}"):
            os.makedirs(f".data/{Game_Name}")

        if platform.system() == 'Windows':
            subprocess.Popen(['attrib','+H','.data'],shell=True)

        if Data.name != None:
                with open(f".data/{Game_Name}/{Data.name}.bin","wb") as f:
                    f.write(Aes.encrypt(dill.dumps(Data), Data.passwd))

    def Load(Game_Name,Name = None,Passwd = None):

        while True:
            if Name == None:
                Name = input('\nUser name:')

            if os.path.isfile(f".data/{Game_Name}/{Name}.bin"):
                break
            else:
                print(f"The user `{Name}' doesn't exists.")
            return

        for i in range(3):
            if Passwd == None:
                Passwd = hashlib.sha256(getpass(prompt='Password:',stream=sys.stderr).encode()).hexdigest()

            with open(f".data/{Game_Name}/{Name}.bin", "rb") as f:
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
                return
            else:
                print('Sorry, try again.')

        return Data

    def Creat(Game_Name,Name = None,Passwd = None):
        while True:
            if Name == None:
                Name = input('\nNew user name:')

            if not os.path.isfile(f".data/{Game_Name}/{Name}.bin"):
                break
            else:
                print(f"The user `{Name}' already exists.")
                return

        while True:
            if Passwd == None:
                Passwd = hashlib.sha256(getpass(prompt='New Password:',stream=sys.stderr).encode()).hexdigest()
                Passwd_Check = hashlib.sha256(getpass(prompt='Retype new Password:',stream=sys.stderr).encode()).hexdigest()
            else:
                Passwd_Check = Passwd

            if Passwd == Passwd_Check:
                break
            else:
                print('Sorry, passwords do not match.')
                Check_Retry = input('Try again? [y/N]')
                while re.search(r'[.*?y.*?|.*?n.*?|1|2]',Check_Retry.lower()) == None:
                    Check_Retry = input(f'ERROR:There is no {Check_Retry} in the choices.\nDo you want to continue? [Y/n] ')
                if re.search(r'[.*?y.*?|1]',Check_Retry.lower()) == None:
                    sys.exit()

        Game_Data = Data(Name, Passwd)
        Passwd = None
        Passwd_Check = None

        return Game_Data