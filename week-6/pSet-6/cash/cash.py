"""
Author: AH-SALAH
cash.py (c) 2021
Desc: add cash.py
Created: 2021-05-17T15:13:20.613Z
Modified: 2021-05-18T09:15:22.438Z
"""

import re
import math


def main():
    co = ""
    while not re.search(r"^\d+([.|,]?)(\d+)=?$", co):
        co = input("Change owed: ")

    # print(f"co: {float(co)}")
    calcCents(float(co))


def calcCents(input):
    """calc cents or dims count

    Args:
        input (float): client currency input
    """
    # tracker = round((input / 100) * 100 if input > 0.999999 else input * 100)
    tracker = round(input * 100)
    coins = 0
    count = 0

    print("Coin Type:\t", end="")

    dimeVal = 25
    for i in range(25, 0, -1):
        # if dime through those available dimes, calc
        if dimeVal == 25 or dimeVal == 10 or dimeVal == 5 or dimeVal == 1:
            count = 0
            cCount = 1
            # while this dime still can be deducted update counts
            while cCount <= math.floor(tracker / dimeVal):
                cCount += 1
                coins += 1
                count = cCount - 1
            # reduce ttl amount by dime that was applicable to be deducted
            tracker %= dimeVal

            # print(f"dimeVal: {dimeVal} floor: {math.floor(tracker / dimeVal)} count: {count} tracker: {tracker}")

            if count >= 1:
                print(f"{dimeVal}c x{count}\t", end="")
            else:
                print("------\t", end="")

        dimeVal = i - 1

    print(f"\nTotal Coins: {coins}")
    print(f"{coins}")


if __name__ == "__main__":
    main()
