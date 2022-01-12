def toDict(data):
    dta = data
    rows = []
    i = 0
    for row in dta:
        obj = {}
        for col in row:
            obj[dta.description[i][0]] = col
            i += 1
        rows.append(obj)
        i = 0
    return rows
