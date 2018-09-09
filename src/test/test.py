#/usr/bin/python3
from time import sleep
import sys, os

frames = ["|", "/", "-", "\\", "|", "/", "-", "\\"]


while True:
    for i in frames:
        sys.stdout.write('\b\b\b')
        sys.stdout.write("[" + i + "]")
        sys.stdout.flush()
        sleep(0.3)
