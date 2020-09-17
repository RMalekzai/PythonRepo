import time
import people
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np


Bob = people.Human(20, 5, (0,0))

X = Bob.location[0]
Y = Bob.location[1]

fig, ax= plt.subplots()

dot = plt.plot(X,Y,"ro")


def animate(x):
    x = Bob.move()
    dot.set_data(x[0], y[1])
    return dot


myAnimation = anim.FuncAnimation(fig, animate, interval=10, blit=True, repeat=True)

plt.show()
