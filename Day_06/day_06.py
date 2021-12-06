#!/usr/bin/env python3


# Could trim this down:
input_file = open("Day_06/input", "r")
lines = [x for x in input_file.readlines()]
# lines = ["3,4,3,1,2"]


# Part 1
print("Part 1:")
fish_list = [int(x) for x in lines[0].split(",")]

for _day in range(80):
    new_fish_list = []
    for i, fish in enumerate(fish_list):
        if fish <= 0:
            fish_list[i] = 6
            new_fish_list.append(8)
        else:
            fish_list[i] -= 1
    fish_list += new_fish_list

part_01 = len(fish_list)
print(f"Result: {part_01}")

# Part 2
print("Part 2:")
fish_list = [int(x) for x in lines[0].split(",")]

# Need more efficient approach
days_left_diff = [0] * 9

for fl in fish_list:
    days_left_diff[fl] += 1

for _day in range(256):
    new_fish = days_left_diff.pop(0)
    days_left_diff.append(new_fish)
    days_left_diff[6] += new_fish

part_02 = sum(days_left_diff)
print(f"Result: {part_02}")
