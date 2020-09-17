import pandas as pd
import random

Units = pd.read_excel(r"C:\Users\roman\PythonRepo\40k Resolver\DataSheets.xlsx", sheet_name="Units")
Weapons = pd.read_excel(r"C:\Users\roman\PythonRepo\40k Resolver\DataSheets.xlsx", sheet_name="Weapons")


def roll_d6(number):
    rolls = []
    for x in range(number):
        rolls.append(random.randint(1,6))
    return rolls


def roll_hits(number, BS):
    hits = 0
    rolls = roll_d6(number)
    for x in rolls:
        if x >= BS:
            hits += 1
    return hits, rolls
