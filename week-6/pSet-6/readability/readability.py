"""
Author: AH-SALAH
readability.py (c) 2021
Desc: add readability.py
Created: 2021-05-18T14:28:18.783Z
Modified: 2021-05-18T19:05:50.746Z
"""

from os import remove
import re


def main():
    str = ""
    while len(str) <= 0 or str.isspace():
        str = input("Text: ")

    getLvls(str)


def getLvls(str):
    """get grade lvl

    Args:
        str (string): input string

    Returns:
        [bool]: returns true
    """
    ttlChar = len([i for i in str if i.isalpha()])
    ttlW = len(str.split(" "))
    ttlS = len([i for i in re.split('\.|\!(?!")|\?(?!\")', str) if "" != i])

    # print([i for i in str if i.isalpha()])
    # print(str.split(" "))
    # print([i for i in re.split("\.|\!(?!\")|\?(?!\")", str) if "" != i])

    # print(f"{ttlChar} Letter(s)")
    # print(f"{ttlW} Word(s)")
    # print(f"{ttlS} Sentence(s)")

    getLvlGrd(ttlChar, ttlW, ttlS)

    return 1


def getLvlGrd(c, w, s):
    """calc lvl grade

    Args:
        c (str): total chars
        w (str): total words
        s (str): total sentences

    Returns:
        [bool]: returns true
    """
    if (not c and not w and not s) or w == 0:
        return 0

    # calc average letters - senetences
    # by Coleman-Liau formula index
    avgL = (float(c) / float(w)) * 100
    avgS = (float(s) / float(w)) * 100
    index = round(0.0588 * avgL - 0.296 * avgS - 15.8)

    # print(f"avgL: {avgL}\navgS: {avgS}\nindex: {index}")

    if index > 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {int(index)}")

    return 1


if __name__ == "__main__":
    main()
