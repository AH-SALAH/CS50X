"""
Author: AH-SALAH
hello.py (c) 2021
Desc: add hello.py
Created: 2021-05-17T11:03:31.022Z
Modified: 2021-05-17T13:00:33.609Z
"""
import sys
import re as regex


def main():
    if len(sys.argv) != 1:
        sys.exit("Usage: py/python <FileName>")

    val = ""
    while not regex.search(r"[a-zA-Z]", val):
        val = input("What is your name?\n")

    print(f"Hello, {val}")


if __name__ == "__main__":
    main()
