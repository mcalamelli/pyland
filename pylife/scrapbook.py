# -*- coding: utf-8 -*-
from threading import Timer


class Something:
    def my_callback(self, arg_a):
        print(arg_a)


class SomethingElse:
    def __init__(self, callback):
        self.callback = callback


something = Something()
something_else = SomethingElse(something.my_callback)
something_else.callback("It works...")


def hello():
    print("hello, world")


t = Timer(30.0, hello)
t.start()  # dopo 30 secondi, sarà stampato "hello, world"
