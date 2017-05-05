#!/usr/bin/python
__author__ = 'kalcho'


import os

def run(**args):
    print "[*] In environment module."
    return str(os.environ)
