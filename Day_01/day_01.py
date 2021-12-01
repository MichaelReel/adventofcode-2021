#!/usr/bin/env python3

input_file = open("Day_01/input", "r")
lines = [int(x.strip()) for x in input_file.readlines()]

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

last_items = lines[:-1]
next_items = lines[1:]
increases = [next for last, next in zip(last_items, next_items) if next > last]
part_01 = len(increases)

print(f"Result: {part_01}")


# Part 2
print("Part 2:")

windows = [
    lines[:-2],
    lines[1:-1],
    lines[2:],
]

sums = [sum(window) for window in zip(*windows)]
last_items = sums[:-1]
next_items = sums[1:]
increases = [next for last, next in zip(last_items, next_items) if next > last]

part_02 = len(increases)
print(f"Result: {part_02}")
