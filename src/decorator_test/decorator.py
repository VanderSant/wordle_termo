#!/usr/bin/env python3
#coding=utf-8

class uppercase():
    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        self.f(args[0].upper())

class star():
    def __init__(self,f):
        self.f = f
    
    def __call__(self,*arg):
        print("*"*30)
        self.f(arg[0])
        print("*"*30)

def star2(f):
    def inner(*arg):
        print("&"*30)
        f(arg[0])
        print("&"*30)
    return inner

@star
@star2
@uppercase
def nome(nome):
    print("Nome: ", nome)


nome("Fulano")