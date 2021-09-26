import random
from my_module import Cards


def str_to_float(Input_phrase):  #入力がstr型となった際にfloat型に変更
    while type(Input_phrase) == str:

        try:
            Input_phrase = float(Input_phrase.replace(',',''))  #コロンを削除
        except ValueError:  #文字列がある場合再度入力を求める
            print("Please input numbers without letters")
            Input_phrase = input()

    return Input_phrase

try:
    while True:

        pass
except KeyboardInterrupt:
    pass