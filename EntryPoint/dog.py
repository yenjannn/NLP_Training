#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cat

whoamiSTR = "This is a wild dog in the global scope."
#這是在 Entry Point 程式進入點之外，在 global scope 晃來晃去的流浪狗

def whoami():
    print(whoamiSTR)

def makeSound():
    return "arf"

if __name__ == "__main__":
    print("This is dog.py")
    print("Puppy makes sound '{}'".format(makeSound()))
    whoamiSTR = "This is a local puppy."
    #這是在 Entry Point 程式進入點「以內」，在地原產的小狗！

    #執行 dog.py 時，程式走到 whoami() 的時候…
    whoami()
    #在 Entry Point 程式進入點以內的 "whoamiSTR"，會指向在地原廠的小狗。

    #相對地，當我們使用「外部呼叫 cat」的方式，而非 「執行 cat.py」的方式，讓程式執行 cat 裡的 whoami() 時
    cat.whoami()
    #程式只能「外部呼叫在進入點之外，在 global scope 裡晃來晃去的流浪貓」。