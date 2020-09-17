import random


class Human():
    def __init__(self, age, movement, location):
        self.age = age
        self.movement = movement
        self.location = location

    def move(self):
        """Take current location and move some random distance in X and Y"""
        (x,y) = (self.location[0], self.location[1])
        return (x+ random.randint(-self.movement, self.movement), y + random.randint(-self.movement, self.movement))

