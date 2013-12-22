#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common
import inspect

def start():
    print("In Function {0}".format(inspect.stack()[0][3]))

def prep():
    print("In Function {0}".format(inspect.stack()[0][3]))

def cleanup():
    print("In Function {0}".format(inspect.stack()[0][3]))

def main():
    print("In Function {0}".format(inspect.stack()[0][3]))

    prep()

    try:
        start()
    except:
        print("Error")

    cleanup()

if __name__=='__main__':
    main()
