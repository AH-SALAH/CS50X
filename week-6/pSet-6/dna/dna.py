"""
Author: AH-SALAH
dna.py (c) 2021
Desc: add dna.py
Created: 2021-05-19T01:18:15.315Z
Modified: 2021-05-22T19:20:52.614Z
"""
import csv
import re
import sys


def main():
    # chk input args
    filesArgs = chkArgs()
    # open csv file
    csv = openCsv(filesArgs[0], "both")
    # open txt file
    txt = openTxt(filesArgs[1])

    # cache csv headers names of STRs
    # also STR string from txt file DNA STR
    headers = csv["list"][0]
    strs = txt[0][0]

    # find all DNA STR which matches with csv headers and add to matchedStr
    matchedStr = getStrCount(headers, strs)

    # compare matching
    compareMatched(matchedStr, csv, headers)


#####################
def getStrCount(headers, strs):
    """Get a STR and DNA String and retrn a matched dict

    Args:
        headers (list): STR Strings
        strs (string): DNA String Sequence

    Returns:
        [dict]: matched dict
    """
    # find all DNA STR which matches with csv headers and add to matchedStr
    matchedStr = {}
    # loop through headers & start from 1 to bypass name col field
    for i in range(1, len(headers)):
        # STR name
        pstr = headers[i]

        # get sequence of STR from the STR string sequence in cached txt file strs
        dna = re.finditer(
            pstr + "(=?(" + pstr + ")+)?", strs, flags=re.IGNORECASE | re.MULTILINE
        )

        if dna:
            for x in dna:
                # x.group is a STR sequence found,
                # l is (the str sequence string length / STR word length)
                # gives sequence count for the STR word in this DNA str sequence
                l = round(len(x.group()) / len(pstr))
                # if same str name already exist, check for length
                if pstr in matchedStr:
                    # if str length is more than the exists, update
                    if l > matchedStr[pstr]:
                        matchedStr[pstr] = l
                else:
                    # else set it in matched rec
                    matchedStr[pstr] = l

    # if found no matched STR, void
    if not len(matchedStr):
        print("No match")
        exit(1)

    return matchedStr


################
def compareMatched(matchedStr, csv, headers):
    """Compare two dict

    Args:
        matchedStr (dict): matched STR dict
        csv (list): list of individual dict
        headers (list): list of STR strings
    """
    rec = 0
    # for every dict row
    for x in csv["dict"]:
        # for every matched str
        # for k in previous cached matched STR
        for k in matchedStr:
            # if matched sequence # found with same key, add to record
            if matchedStr[k] == x[k]:
                rec += 1
        # if same rec counts matched, then all headers matched = seems catched 🕵
        if rec == len(headers) - 1:  # headers -1 to negate 'name' cell out of counting
            print(x["name"])  # 😎
            break  # 📌 👉
        # if didn't matched, reset rec to count another individual
        rec = 0

    # if no records, then no match 🙄
    if not rec:
        print("No match")
        exit(1)


#################
def openCsv(file, respType="dict", mode="r"):
    """open csv file

    Args:
        file (stream): file to open
        respType (str, optional): dict | both | "". Defaults to "dict".
        mode (str, optional): file operation mode. Defaults to "r".

    Returns:
        list: data
    """

    if not file:
        return

    dictList = []
    li = []
    data = []

    d = openFiles(file, respType, mode)
    # v = [d[k] for k in ('dict', 'list')]

    # add data to list
    li = [i for i in d["list"]]

    # add data to dicList
    dictList = [x for x in d["dict"]]

    # change string numbers to digits
    data = toDigits(dictList, li)

    return data


############################
def openTxt(file, respType="", mode="r"):
    """open txt file

    Args:
        file (stream): file to open
        respType (str, optional): dict | both | "". Defaults to "".
        mode (str, optional): file operation mode. Defaults to "r".

    Returns:
        list: data
    """
    if not file:
        return

    data = openFiles(file, respType, mode)

    return data


##############
def chkArgs():
    """check sysArgs correctness

    Returns:
        list: list files strings
    """
    errMsg = "Usage: <filename> file.csv text.txt"
    correctLen = len(sys.argv) == 3

    if not correctLen:
        print(errMsg)
        exit(1)

    csv = re.search("\.csv$", sys.argv[1])
    txt = re.search("\.txt$", sys.argv[2])

    if not csv or not txt:
        print(errMsg)
        exit(1)

    return [sys.argv[1], sys.argv[2]]


#####################
def toDigits(dictList=[], li=[]):
    """convert string numbers to digits inside list of dict or list of lists

    Args:
        dicList (list): list of dict
        li (list): list of lists

    Returns:
        dict: dict of dict and list of lists with names dictList and li respectivley
    """
    chk = not len(dictList) and not len(li)
    if chk:
        print("toDigits doesn't got needed args!")
        return {}

    d = []
    l = []

    # chk for any of args
    # verify & change string numbers to digits

    if dictList and (type(dictList) is list) and len(dictList):
        d = [x for x in dictList]
        for x in d:
            for i in x:
                if x[i].isdigit():
                    x[i] = int(x[i])
                    # print("i: ", x[i])

    if li and (type(li) is list) and len(li):
        l = [k for k in li]
        for x in l:
            for j in range(len(x)):
                if x[j].isdigit():
                    x[j] = int(x[j])
                    # print("j: ", j)

    # print("dicList: ", dicList)

    # return the new data modified
    return {"dict": d, "list": l}


##############################################
def openFiles(file, respType="dict", mode="r"):
    """open files

    Args:
        file (stream): file to open
        respType (str, optional): file type options[dict or both or ""]. Defaults to "dict".
        mode (str, optional): read mode. Defaults to "r".

    Returns:
        data of the read stream: content data
    """
    data = []
    # open the file with the predefined file response datatype
    with open(file, mode) as f:
        if respType == "dict":
            data = [i for i in csv.DictReader(f)]
        elif respType == "both":
            r = [x for x in csv.reader(f)]
            f.seek(0)  # solved reading with multiple reader types
            d = [i for i in csv.DictReader(f)]

            data = {"dict": d, "list": r}
        else:
            data = [x for x in csv.reader(f)]

    return data


#########################
if __name__ == "__main__":
    main()
