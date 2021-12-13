#!/usr/bin/env python3
from collections import namedtuple


input_file = open("Day_13/input", "r")
# input_file = open("Day_13/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]

Dot = namedtuple('Dot', 'x y')

dots = set()
folds = []
line_index = 0
while lines[line_index] != "":
    x, y = lines[line_index].split(",")
    dots.add(Dot(int(x),int(y)))
    line_index += 1
line_index += 1
for line in lines[line_index:]:
    line = line.strip("fold along ")
    axis, index = line.split("=")
    folds.append((axis, int(index)))

# print(f"{dots}\n\n{folds}\n\n")

# Part 1
print("Part 1:")

# Do first fold
new_dots = set()
axis, index = folds.pop(0)
if axis == "x":
    for dot in dots:
        if dot.x > index:
            new_dots.add(Dot(index * 2 - dot.x, dot.y))
        else:
            new_dots.add(dot)
if axis == "y":
    for dot in dots:
        if dot.y > index:
            new_dots.add(Dot(dot.x, index * 2 - dot.y))
        else:
            new_dots.add(dot)


# print(f"{new_dots}\n\n{folds}\n\n")

part_01 = len(new_dots)
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

# do rest of folds
display_x, display_y = 0, 0
dots = new_dots
while folds:
    new_dots = set()
    axis, index = folds.pop(0)
    if axis == "x":
        display_x = index
        for dot in dots:
            if dot.x > index:
                new_dots.add(Dot(index * 2 - dot.x, dot.y))
            else:
                new_dots.add(dot)
    if axis == "y":
        display_y = index
        for dot in dots:
            if dot.y > index:
                new_dots.add(Dot(dot.x, index * 2 - dot.y))
            else:
                new_dots.add(dot)
    dots = new_dots


# print(f"{new_dots}\n\n{folds}\n\n")

# Make display
display_str = ""
for y in range(display_y):
    for x in range(display_x):
        display_str += "#" if Dot(x, y) in dots else " "
    display_str += "\n"


part_02 = "\n" + display_str
print(f"Result: {part_02}")
