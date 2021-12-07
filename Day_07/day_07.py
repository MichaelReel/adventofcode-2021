#!/usr/bin/env python3


input_file = open("Day_07/input", "r")
lines = [x for x in input_file.readlines()]
# lines = ["16,1,2,0,4,2,7,1,2,14"]

crab_list = [int(x) for x in lines[0].split(",")]
min_hortz_pos = min(crab_list)
max_hortz_pos = max(crab_list)

# Part 1
print("Part 1:")

# Naive solution
min_cost = 9223372036854775807  # 2^63-1
min_cost_pos = -1
for hortz_pos in range(min_hortz_pos, max_hortz_pos + 1):
    cost = sum([abs(hortz_pos - x) for x in crab_list])
    if cost < min_cost:
        min_cost = cost
        min_cost_pos = hortz_pos

part_01 = min_cost
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

def crab_cost(start: int, end: int) -> int:
    """Basically a triangle number, no need for a loop here"""
    dx = abs(start - end)
    return (dx * (dx + 1)) / 2

min_cost = 9223372036854775807  # 2^63-1
min_cost_pos = -1
for hortz_pos in range(min_hortz_pos, max_hortz_pos + 1):
    cost = sum([crab_cost(hortz_pos, x) for x in crab_list]) 
    if cost < min_cost:
        min_cost = cost
        min_cost_pos = hortz_pos

part_02 = int(min_cost)
print(f"Result: {part_02}")
