#!/usr/bin/env python3

from itertools import filterfalse


input_file = open("Day_01/input", "r")
lines = [x.strip() for x in input_file.readlines()]
# lines = [
#     199,
#     200,
#     208,
#     210,
#     200,
#     207,
#     240,
#     269,
#     260,
#     263,
# ]

# Part 1
print("Part 1:")

part_01 = 0
for i, item in enumerate(lines[:-1]):
    item_1 = lines[i + 1]
    part_01 += 1 if item_1 > item else 0
    print(f"{item} <? {item_1}: {part_01}")

print(f"Result: {part_01}")

# Part 2
print("Part 2:")

part_02 = "not implemented yet"
print(f"Result: {part_02}")
