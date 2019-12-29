import matplotlib.pyplot as pp


def add_direction(start, code):
    (x, y) = start
    if code[0] == "U":
        line = [(x, y +i) for i in range(int(code[1:]))]
        return line[1:]
    elif code[0] == "D":
        line = [(x, y - i) for i in range(int(code[1:]))]
        return line[1:]
    elif code[0] == "R":
        line = [(x + i, y) for i in range(int(code[1:]))]
        return line[1:]
    elif code[0] == "L":
        line = [(x - i, y) for i in range(int(code[1:]))]
        return line[1:]
    else:
        print("That didn't work")


first = open(r"C:\Users\roman\PythonRepo\Advent of Code 2019\Day3-1.txt", "r")
second = open(r"C:\Users\roman\PythonRepo\Advent of Code 2019\Day3-2.txt", "r")
first_line = first.read().split(",")
second_line = second.read().split(",")
first.close()
second.close()

# test = open(r"C:\Users\roman\PythonRepo\Advent of Code 2019\D3test.txt", "r")
# testing = test.read().split(",")
# test.close()
grid = []
start = (0, 0)

for x in first_line:
    segment = add_direction(start,x)
    for point in segment:
        if point not in grid:
            grid.append(point)
    start = segment[-1]


start = (0, 0)
grid2 = []

for x in second_line:
    segment = add_direction(start,x)
    for point in segment:
        if point not in grid2:
            grid2.append(point)
    start = segment[-1]


intersections = [x for x in grid if x in grid2]
distances = []

# for point in intersections:
#     (x, y) = point
#     distances.append(abs(x) + abs(y))

print(min(distances))

# fig = pp.figure()
# ax1 = fig.add_subplot(111)
# ax1.scatter([x for (x, y) in grid.keys()], [y for (x, y) in grid.keys()])
# ax1.scatter([x for (x, y) in grid2.keys()], [y for (x, y) in grid2.keys()])
# pp.show()