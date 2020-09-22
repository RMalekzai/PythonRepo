import pandas as pd
import random

Units = pd.read_excel(r"C:\Users\roman\PythonRepo\40k Resolver\DataSheets.xlsx", sheet_name="Units", index_col="Unit")
Weapons = pd.read_excel(r"C:\Users\roman\PythonRepo\40k Resolver\DataSheets.xlsx", sheet_name="Weapons",index_col="Weapon")


def shots(weapon):
    if str.isnumeric(weapon.Shots):
        return weapon.Shots
    else:
        return weapon.Shots[1:]


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
    return hits


def roll_wounds(number, S, T):
    wounds = 0
    rolls = roll_d6(number)
    if S >= T*2:
        wounds += sum([x >= 2 for x in rolls])
        return wounds
    elif S > T:
        wounds += sum([x >= 3 for x in rolls])
        return wounds
    elif S == T:
        wounds += sum([x >= 4 for x in rolls])
        return wounds
    elif T > S:
        wounds += sum([x >= 5 for x in rolls])
        return wounds
    elif T >= S*2:
        wounds += sum([x >= 6 for x in rolls])
        return wounds


def roll_save(number, ap, armour, invul):
    save = min([armour + ap, invul])
    if save > 6:
        return 0
    rolls = roll_d6(number)
    return sum([x >= save for x in rolls])


def shooting(attacker, defender):
    y = shots(attacker.gun)
    hits = roll_hits(y, attacker.BS)
    wounds = roll_wounds(hits, attacker.S, defender.T)
    saved = roll_save(wounds, attacker.AP, defender.Save, defender.Invul)
    print("{0} fired {1} shots, {2} of them hit, {3} of them wounded, and {4} of them were saved.".format(attacker.Unit, y, hits, wounds, saved))
    return wounds - saved


class Model:
    def __init__(self, name, M, BS, S, T, W, A, LD, Save, Ignore, RR_H, RR_W, RR_Dmg, gun, Invul=7):
        self.name = name
        self.M = M
        self.BS = BS
        self.S = S
        self.T = T
        self.W = W
        self.A = A
        self.LD = LD
        self.Save = Save
        self.Invul = Invul
        self.Ignore = Ignore
        self.RR_H = RR_H
        self.RR_W = RR_W
        self.RR_Dmg = RR_Dmg
        self.gun = gun


class Weapon:
    def __init__(self, name, range, type, shots, s, ap, d, ability=""):
        self.name = name
        self.range = range
        self.type = type
        self.shots = shots
        self.s = s
        self.ap = ap
        self.d = d
        self.ability = ability


# for x in Units.Unit:
#     x = Model(x, x.M, x.BS, x.S, x.T, x.W, x.A, x.LD, x.Save, x.Invul, x.Ignore, x.RR_H, x.RR_W, x.RR_Dmg)

