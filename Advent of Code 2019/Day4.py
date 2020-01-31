"""
    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
    Range = 273025-767253
"""
Prange = [x for x in range(273025, 767253 + 1)]
possibles = []


def increasing_digits(num):
    query = [x for x in str(num)]
    for x in range(len(query)-1):
        if int(query[x]) <= int(query[x+1]):
            continue
        else:
            return False
    return True


def repeating_digits(num):
    query = [x for x in str(num)]
    for x in range(len(query)-1):
        if int(query[x]) == int(query[x+1]):
            if int(query[x]) == int(query[x-1]):
                continue
            else:
                return True
    return False


for x in Prange:
    if increasing_digits(x) and repeating_digits(x):
        possibles.append(x)


print(len(possibles))
