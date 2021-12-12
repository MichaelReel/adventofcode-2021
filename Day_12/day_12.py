#!/usr/bin/env python3


# input_file = open("Day_12/sample_a_input", "r")
# input_file = open("Day_12/sample_b_input", "r")
# input_file = open("Day_12/sample_c_input", "r")
input_file = open("Day_12/input", "r")
lines = [x.strip() for x in input_file.readlines()]


connections = {}
for line in lines:
    left, right = line.split("-")
    # Bet there's some one-liner that'll do this:
    if left in connections:
        connections[left].append(right)
    else:
        connections[left] = [right]
    if right in connections:
        connections[right].append(left)
    else:
        connections[right] = [left]

# Part 1
print("Part 1:")

def traverse_caves(current_path: list[str], connections: dict[str,str]) -> list[list[str]]:
    current_cave = current_path[-1]
    if current_cave == "end":
        return [current_path]
    next_caves = connections[current_cave]
    next_paths = []
    for next_cave in next_caves:
        # ignore small caves we visited already
        if next_cave.lower() == next_cave and next_cave in current_path:
            continue
        next_paths += traverse_caves(current_path + [next_cave], connections)
    return next_paths

all_paths = traverse_caves(["start"], connections)
# print(f"{all_paths}")


part_01 = len(all_paths)
print(f"Result: {part_01}")

# Part 2
print("Part 2:")


def traverse_caves_2(current_path: list[str], connections: dict[str,str]) -> list[list[str]]:
    current_cave = current_path[-1]
    if current_cave == "end":
        return [current_path]
    next_caves = connections[current_cave]
    next_paths = []
    for next_cave in next_caves:
        # ignore small caves we visited already
        if next_cave.lower() == next_cave and next_cave in current_path:
            # In paticular if it's the start (or end) cave
            if next_cave == "start" or next_cave == "end":
                continue
            # And if there has been a small cave visited twice already
            small_caves_in_path = [cave for cave in current_path if cave.lower() == cave]
            if len(small_caves_in_path) != len(set(small_caves_in_path)):
                continue
        next_paths += traverse_caves_2(current_path + [next_cave], connections)
    return next_paths

all_paths = traverse_caves_2(["start"], connections)
# for path in all_paths:
#     print(f"{path}")

part_02 = len(all_paths)
print(f"Result: {part_02}")
