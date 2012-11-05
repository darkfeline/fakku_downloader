#!/usr/bin/env python3

import subprocess
import os
import time
from random import choice

def main(*args):
    stuff = os.listdir()
    while len(stuff) > 0:
        pick = choice(stuff)
        stuff.remove(pick)
        print(pick)
        time.sleep(1)
        subprocess.call(('feh', '-F', '--cycle-once', pick))

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
