#!/usr/bin/env python3
from collections import namedtuple
from re import match



input_file = open("Day_17/input", "r")
# input_file = open("Day_17/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]

# print(f"{lines[0]}")

trench_input = match(r"^target area: x=(?P<x_min>-?\d+)..(?P<x_max>-?\d+), y=(?P<y_min>-?\d+)..(?P<y_max>-?\d+)$", lines[0]).groupdict()
# print(f"{trench_input}")

x_min = int(trench_input["x_min"])
x_max = int(trench_input["x_max"])
y_min = int(trench_input["y_min"])
y_max = int(trench_input["y_max"])

Point = namedtuple("Point", "x y")


# Lets naively try out a bunch of trajectories
apogee_list = []
# First initial velocity.y that can hit is y_min, any lower will overshoot
# Just guessing the upper bound here
for dy in range(y_min, 100):
    # Min x is zero, i.e. dropped staight down or thrown straight up
    # Last initial velocity that can hit is x_max, any higher will overshoot
    for dx in range(0, x_max + 1):
        apogee = 0
        velocity = Point(x=dx, y=dy)
        pos = Point(x=0, y=0)
        # Apply velocity until we overshoot:
        while pos.x < x_max and pos.y > y_min:
            pos = Point(x=pos.x + velocity.x, y=pos.y + velocity.y)
            apogee = max(pos.y, apogee)
            # Test trench entry
            if pos.x >= x_min and pos.x <= x_max and pos.y >= y_min and pos.y <= y_max:
                apogee_list.append(apogee)
                # print(f"Point in trench: {pos}, apogee was: {apogee}, for starter velocity ({dx},{dy})")
                break
            # Apply acceleration to the velocity
            new_velocity_x = 0
            if velocity.x > 0:
                new_velocity_x = velocity.x - 1
            elif velocity.x < 0:
                new_velocity_x = velocity.x + 1
            velocity = Point(new_velocity_x, velocity.y - 1)

# Part 1
print("Part 1:")

part_01 = max(apogee_list)
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

part_02 = len(apogee_list)
print(f"Result: {part_02}")
