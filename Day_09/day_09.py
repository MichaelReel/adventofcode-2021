#!/usr/bin/env python3


from itertools import product


input_file = open("Day_09/input", "r")
lines = [x.strip() for x in input_file.readlines()]
# lines = [
#     "2199943210",
#     "3987894921",
#     "9856789892",
#     "8767896789",
#     "9899965678",
# ]

low_points = []

# Part 1
print("Part 1:")

def get_neighbours(lines:list[str], x:int, y:int) -> list[int]:
    neighbours = []
    if x > 0:
        neighbours.append(int(lines[y][x-1]))
    if x < len(lines[y]) - 1:
        neighbours.append(int(lines[y][x+1]))
    if y > 0:
        neighbours.append(int(lines[y-1][x]))
    if y < len(lines) - 1:
        neighbours.append(int(lines[y+1][x]))
    return neighbours

risk_level_total = 0
for y in range(len(lines)):
    for x in range(len(lines[0])):
        height = int(lines[y][x])
        neighbours = get_neighbours(lines, x, y)
        if min(neighbours) > height:
            low_points.append((x, y))
            risk_level_total += height + 1
        

part_01 = risk_level_total
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

visited = set()
# For each low point from part 01, get it's basin score
def get_basin(lines:list[str], x:int, y:int) -> list[int]:

    # print(f"basin visit: {x, y}, visited: {visited}")
    if (x,y) in visited:
        return []
    visited.add((x,y))
    if int(lines[y][x]) == 9:
        return []
    basin = [(x, y)]
    if x > 0:
        basin += get_basin(lines, x-1, y)
    if x < len(lines[y]) - 1:
        basin += get_basin(lines, x+1, y)
    if y > 0:
        basin += get_basin(lines, x, y-1)
    if y < len(lines) - 1:
        basin += get_basin(lines, x, y+1)
    return basin

basin_sizes = []
for low_point in low_points:
    basin = get_basin(lines, *low_point)
    basin_sizes.append(len(basin))

basin_sizes = sorted(basin_sizes)
# print(f"{basin_sizes}")

part_02 = basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]
print(f"Result: {part_02}")
