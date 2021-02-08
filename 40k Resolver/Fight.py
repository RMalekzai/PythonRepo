import pandas as pd
import random

Units = pd.read_excel(r"C:\Users\roman\PythonRepo\40k Resolver\DataSheets.xlsx", sheet_name="Units")
Weapons = pd.read_excel(r"C:\Users\roman\PythonRepo\40k Resolver\DataSheets.xlsx", sheet_name="Weapons")


class Model:
    def __init__(self, name, M, WS, BS, S, T, W, A, LD, Save, Ignore = 0, RR_H=0, RR_W=0, RR_Dmg=0, Invul=0):
        self.name = name
        self.M = M
        self.WS = WS
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


class Gun:
    def __init__(self, name, range, type, shots, s, ap, d, ability=""):
        self.name = name
        self.range = range
        self.type = type
        self.shots = shots
        self.s = s
        self.ap = ap
        self.d = d
        self.ability = ability


"""This section makes an entry in the Models dictionary, where Key is the Model name and the value is the class instance
for each line in the data sheet excel"""
Models = {}
for x in Units.index:
    stats = Units.loc[x]
    Models[str(stats[1])] = Model(str(stats[1]), stats[2], stats[3], stats[4], stats[5], stats[6], stats[7], stats[8],
                                  stats[9], stats[10], stats[12], stats[13], stats[14], stats[15])

Guns = {}
for x in Weapons.index:
    stats = Weapons.loc[x]
    Guns[str(stats[0])] = Gun(stats[0], stats[2], stats[3], stats[4], stats[5], stats[6], stats[7], stats[8])


HavocSquad = [(Models["Havoc"], "HBolter"), (Models["Havoc"], "HBolter"), (Models["Havoc"], "ReaperC"),
              (Models["Havoc"], "ReaperC"), (Models["Aspiring Champion H"], "CombiBolter")]

CSM_Squad_Bolters = [(Models["Chaos Space Marine"], "Bolter"), (Models["Chaos Space Marine"], "Bolter"),
                     (Models["Chaos Space Marine"], "Bolter"), (Models["Chaos Space Marine"], "Bolter"),
                     (Models["Aspiring Champion CSM"], "Bolter")]


def roll_d6(number):
    rolls = []
    for x in range(number):
        rolls.append(random.randint(1, 6))
    return rolls


def roll_dx(x):
    return random.randint(1, x)


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
    elif T >= S * 2:
        wounds += sum([x >= 6 for x in rolls])
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


def roll_save(number, ap, armour, invul):
    if invul:
        save = min(armour + ap, invul)
    else:
        save = armour + ap
    if save > 6:
        return 0
    rolls = roll_d6(number)
    return sum([x >= save for x in rolls])


def calc_damage(Whits, gun, defender):
    ignore = defender.Ignore
    damage = 0
    if type(gun.d) == int:
        damage += gun.d * Whits
    elif type(gun.d) == str:
        for x in range(Whits):
            damage += roll_dx(int(gun.d[1:]))
    return damage


"""Shoots one model at one other model, but i guess it's good for now"""
def shooting(attacker, defender):
    i, j = defender
    i.Gun = j
    m, n = attacker
    m.Gun = n
    for gun in m.Gun:
        if type(gun.shots) == int:
            y = gun.shots
        else:
            y = roll_dx(int(gun.shots[1:]))
        hits = roll_hits(y, m.BS)
        wounds = roll_wounds(hits, gun.s, i.T)
        saved = roll_save(wounds, gun.ap, i.Save, i.Invul)
        Whits = wounds - saved
        damage = calc_damage(Whits, gun, i)
        print("{0} fired {1} shots with a {2}, {3} of them hit, {4} of them wounded, and {5} of them were saved. "
              "Total wounding hits: {6}, Total Damage: {7}."
              .format(m.name, y, gun.name, hits, wounds, saved, Whits, damage))

    for gun in i.Gun:
        if type(gun.shots) == int:
            y = gun.shots
        else:
            y = roll_dx(int(gun.shots[1:]))
        hits = roll_hits(y, i.BS)
        wounds = roll_wounds(hits, gun.s, m.T)
        saved = roll_save(wounds, gun.ap, m.Save, m.Invul)
        Whits = wounds - saved
        damage = calc_damage(Whits, gun, m)
        print("{0} fired {1} shots with a {2}, {3} of them hit, {4} of them wounded, and {5} of them were saved. "
              "Total wounding hits: {6}, Total Damage: {7}."
              .format(i.name, y, gun.name, hits, wounds, saved, Whits, damage))


CSM = (Models["Chaos Space Marine"], [Guns["Bolter"]])
Forgefiend = (Models["Forgefiend"], [Guns["HadesAutoCannon"], Guns["HadesAutoCannon"]])

# def shooting(squad1, squad2):
#     Squad1_Models = [x for (x,y) in squad1]
#     Squad1_Guns = [y for (x,y) in squad1]
#     Squad2_Models = [x for (x,y) in squad2]
#     Squad2_Guns = [y for (x,y) in squad2]
