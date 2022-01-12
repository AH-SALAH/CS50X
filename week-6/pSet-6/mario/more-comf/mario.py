"""
Author: AH-SALAH
mario.py (c) 2021
Desc: add mario.py
Created: 2021-05-17T14:54:39.026Z
Modified: 2021-05-17T14:58:34.574Z
"""

import re as regex


def main():
    # get user input while its int from 1-8
    h = ""
    while not regex.search(r"^[1-8]$", h):
        h = input("Height: ")

    j = 0
    x = ""
    s = ""

    # fill empty str by height #
    while j < int(h):
        s += " "
        j += 1

    # print # lines with spaces
    for i in range(j):
        x += "#"
        print(s[: j - 1 - i] + x + "  " + x + "\n", end="")


if __name__ == "__main__":
    main()
