import pandas as pd

# data = open(r"C:\Users\roman\PycharmProjects\FunProjects\Advent of Code 2019\Day1 Data.txt", 'r')
# components = [line for line in data.readlines()]
# data.close()
df = pd.read_excel(r"C:\Users\roman\Documents\components.xlsx", dtype=int)


def calc_fuel(x):
    return (x//3)-2


def fuel_count(comps):
    total = 0
    for x in comps:
        y = calc_fuel(x)
        while y >0:
            total += y
            y = calc_fuel(y)
    return total


print(fuel_count(df.weight))