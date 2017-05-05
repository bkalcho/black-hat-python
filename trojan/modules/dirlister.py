#!/usr/bin/python
__author__ = 'kalcho'


import os

def run(**args):
    print "[*] In dirlister module."
    files = os.listdir(".")

    return str(files)
