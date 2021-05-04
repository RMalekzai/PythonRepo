import pandas as pd
import random

Units = pd.read_excel(r"C:\Users\roman\PythonRepo\40k Resolver\DataSheets.xlsx", sheet_name="Units")
Weapons = pd.read_excel(r"C:\Users\roman\PythonRepo\40k Resolver\DataSheets.xlsx", sheet_name="Weapons")


class Model:
    def __init__(self, name, M, WS, BS, S, T, W, A, LD, Save, Ignore = 0, RR_H=7, RR_W=7, RR_Dmg=0, Invul=0):
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
                                  stats[9], stats[10], stats[12], stats[13], stats[14], stats[15], stats[11])

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


def roll_hits(number, BS, RR_H):
    hits = 0
    rerolls = []
    rolls = roll_d6(number)
    for x in rolls:
        if x < BS and x <= RR_H:
            rerolls.append(roll_dx(6))
        elif x >= BS:
            hits += 1
    for y in rerolls:
        if y >= BS:
            hits += 1
    return hits


def roll_wounds(number, attacker, S, T, RR_W):
    wounds = 0
    rerolls = []
    if type(S) == str:
        if "+" in S:
            S = attacker.S + S[1:]
        elif "User" in S:
            S = attacker.S
    rolls = roll_d6(number)
    if S >= T*2:
        # wounds += sum([x >= 2 for x in rolls])
        # return wounds
        woundon = 2
    elif T >= S * 2:
        # wounds += sum([x >= 6 for x in rolls])
        # return wounds
        woundon = 6
    elif S > T:
        # wounds += sum([x >= 3 for x in rolls])
        # return wounds
        woundon = 3
    elif S == T:
        # wounds += sum([x >= 4 for x in rolls])
        # return wounds
        woundon = 4
    elif T > S:
        # wounds += sum([x >= 5 for x in rolls])
        # return wounds
        woundon = 5
    for x in rolls:
        if x < woundon and x <= RR_W:
            rerolls.append(roll_dx(6))
        elif x >= woundon:
            wounds += 1
    for y in rerolls:
        if y >= woundon:
            wounds += 1
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


def calc_damage(Whits, gun):
    damage = 0
    if type(gun.d) == int:
        damage += gun.d * Whits
    elif type(gun.d) == str and "+" not in gun.d:
        for x in range(Whits):
            damage += roll_dx(int(gun.d[1:]))
    elif type(gun.d) == str and "+" in gun.d:
        for x in range(Whits):
            damage += roll_dx(int(gun.d[1:2])) + int(gun.d[-1])
    return damage


def calc_fnp(defender, damage):
    ignore = defender.Ignore
    rolls = roll_d6(damage)
    saved = 0
    for x in rolls:
        if x >= ignore:
            saved += 1
    return damage-saved, saved


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
        hits = roll_hits(y, m.BS, m.RR_H)
        wounds = roll_wounds(hits, m, gun.s, i.T, m.RR_W)
        saved = roll_save(wounds, gun.ap, i.Save, i.Invul)
        Whits = wounds - saved
        damage = calc_damage(Whits, gun)
        FnP = calc_fnp(i, damage)
        print("{0} fired {1} shots with a {2}, {3} of them hit, {4} of them wounded, and {5} of them were saved. "
              "Total wounding hits: {6}, Total Damage: {7}. {8} wounds saved with FnP, {9} wounds lost"
              .format(m.name, y, gun.name, hits, wounds, saved, Whits, damage, FnP[1], FnP[0]))

    for gun in i.Gun:
        if type(gun.shots) == int:
            y = gun.shots
        else:
            y = roll_dx(int(gun.shots[1:]))
        hits = roll_hits(y, i.BS, i.RR_H)
        wounds = roll_wounds(hits, i, gun.s, m.T, i.RR_W)
        saved = roll_save(wounds, gun.ap, m.Save, m.Invul)
        Whits = wounds - saved
        damage = calc_damage(Whits, gun)
        FnP = calc_fnp(m, damage)
        print("{0} fired {1} shots with a {2}, {3} of them hit, {4} of them wounded, and {5} of them were saved. "
              "Total wounding hits: {6}, Total Damage: {7}. {8} wounds saved with FnP, {9} wounds lost"
              .format(i.name, y, gun.name, hits, wounds, saved, Whits, damage, FnP[1], FnP[0]))


CSM = (Models["Chaos Space Marine"], [Guns["Bolter"]])
Forgefiend = (Models["Forgefiend"], [Guns["HadesAutoCannon"], Guns["HadesAutoCannon"]])
Reaper = (Models["Reaper"], [Guns["StormVP2"]])
GUO = (Models["Great Unclean One"], [Guns["PlagueFlail"]])

# def shooting(squad1, squad2):
#     Squad1_Models = [x for (x,y) in squad1]
#     Squad1_Guns = [y for (x,y) in squad1]
#     Squad2_Models = [x for (x,y) in squad2]
#     Squad2_Guns = [y for (x,y) in squad2]
