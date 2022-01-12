"""
Author: AH-SALAH
credit.py (c) 2021
Desc: add credit.py
Created: 2021-05-18T09:18:02.802Z
Modified: 2021-05-18T14:21:13.204Z
"""

from math import floor


def main():
    n = ""
    validLen = [13, 15, 16]
    errMsg = "INVALID"

    # while input is not a digit or its length not among the specified digits re-prompt
    while not n.isdigit() or len(n) not in validLen:
        n = input("Card #: ")
        if len(n) not in validLen:
            print(errMsg)
            exit(0)

    return isValid(n, errMsg)


def isValid(n, errMsg):
    """chk card invalidity

    Args:
        n (str): card #
        errMsg (str): error msg

    Returns:
        bool: returns false or checksum fn
    """
    f2 = n[:2]
    # lenCache = n
    # len = 0
    errorMsg = errMsg or "Not a Valid Card!"
    type = ""

    # while lenCache >= 0:
    #     if lenCache < 1:
    #         break
    #     else:
    #         lenCache /= 10
    #         len += 1

    # if len != 13 and len != 15 and len != 16:
    #     print(errorMsg)
    #     return 0

    # while f2 > 100:
    #     f2 /= 10

    # print("f22: ", f2)

    switch = {
        51: "MASTERCARD",
        52: "MASTERCARD",
        53: "MASTERCARD",
        54: "MASTERCARD",
        55: "MASTERCARD",
        22: "MASTERCARD",
        34: "AMEX",
        37: "AMEX",
        4: "VISA",
    }

    # get the corresponding card type from the dict if though
    type = switch.get(int(f2))

    # print("if type1: ", type or False)

    # if no card type & still last digit has 2 digits divid more to first number
    if not type and int(f2) >= 10:
        # f2 /= 10
        f2 = n[:1]
        type = switch.get(int(f2))
        # print("type2: ", type, "f23: ", f2)

    # if we got a type then proceed to chksum
    if type:
        # print("type3: ", type)
        return checkSum(n, type, errorMsg)
    else:
        print(errorMsg)
        return 0


def checkSum(n, cType, errMsg):
    """do chksum for card is real card or not

    Args:
        n (str): card #
        cType (str): card type
        errMsg (str): error msg

    Returns:
        bool: true if valid chksum or false otherwise
    """
    errorMsg = errMsg or "Not a Valid Card!"
    tracker = int(n)
    cache1 = 0
    cache2 = 0
    sum1 = 0
    sum2 = 0
    ttl = 0

    while floor(tracker) > 0:
        # multiply second-to-last digit by 2 & sum them
        # and the same for 1st to last without multiplying
        # and then divid card digits by 100 to bypass the calculated to next twos

        # step by 10 & modulo by 10 to get the digit at the start of the whole digit & multiply by 2
        cache1 = floor((tracker / 10) % 10) * 2
        sum1 += (lambda: cache1, lambda: floor((cache1 / 10) + (cache1 % 10)))[
            cache1 > 9
        ]()
        # sum1 += floor((cache1 / 10) + (cache1 % 10)) if cache1 > 9 else cache1
        # get the none multiplied digit
        cache2 = floor(floor((tracker * 10) % 100) / 10)
        sum2 += cache2
        # bypass the 2 digits to next
        tracker /= 100
        # print(f"tracker: {tracker} sum1: {sum1} cache1: {cache1} cache > 9: {cache1 > 9}")
        # print(f"tracker: {tracker} sum2: {sum2} cache2: {cache2}")

    # print("sum1: ", sum1, "sum2: ", sum2)
    # sum the sum of both digits calc
    ttl = sum1 + sum2

    # print("ttl: ", ttl, "ttl%10: ", ttl % 10)

    # if total sum modulo == 0 then its a valid card
    if ttl % 10 == 0:
        print(f"CheckSum total: {ttl} Last Digit: {ttl % 10} Is Valid: true \n")
        print(cType)
        return 1
    else:
        print(errorMsg)

    return 0


if __name__ == "__main__":
    main()
