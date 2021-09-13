#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import dog

print("Cat is imported")
whoamiSTR = "This is a wild cat in the global scope."
#

def whoami():
    print(whoamiSTR)

def makeSound():
    return "meow"

if __name__ == "__main__":
    print("This is cat.py")
    print("Kitty makes sound '{}'".format(makeSound()))
    whoamiSTR = "This is a local kitty."
    #

    #
    whoami()
    #

    #
    dog.whoami()
    #
