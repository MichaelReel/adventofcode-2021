#!/usr/bin/env python3


input_file = open("Day_02/input", "r")
lines = [x for x in input_file.readlines()]

# lines = [
#     "forward 5",
#     "down 5",
#     "forward 8",
#     "up 3",
#     "down 8",
#     "forward 2",
# ]

# Part 1
print("Part 1:")

position = {"x":0, "y":0}
for line in lines:
    movement, units_str = line.split(' ', 1)
    units = int(units_str)
    
    if movement == "forward":
        position["x"] += units
    elif movement == "down":
        position["y"] += units
    elif movement == "up":
        position["y"] -= units

    # print(f"{position}")


part_01 = position["x"] * position["y"]
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

aim = 0
position = {"x":0, "y":0}
for line in lines:
    movement, units_str = line.split(' ', 1)
    units = int(units_str)
    
    if movement == "forward":
        position["x"] += units
        position["y"] += aim * units
    elif movement == "down":
        aim += units
    elif movement == "up":
        aim -= units

    # print(f"{position}")
    
part_02 = position["x"] * position["y"]
print(f"Result: {part_02}")
