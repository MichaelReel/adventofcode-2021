#!/usr/bin/env python3
from itertools import permutations

input_file = open("Day_15/input", "r")
# input_file = open("Day_15/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]
grid = [[int(x) for x in line] for line in lines]

# Part 1
print("Part 1:")

# So, we know we have to go from top left to bottom right
# Every possible path will involve either an incrementation on the X axis or Y axis
height = len(grid)
width = len(grid[0])
# print(f"{width} x {height}")

# Fairly naive approach, just give each grid point a score depending on the square beside it
scores = []
for y in range(height):
    scores.append([])
    for x in range(width):
        local = grid[y][x]
        if x == 0 and y == 0:
            scores[y].append(0)
            continue
        down_score = scores[y-1][x] if y > 0 else 100000
        right_score = scores[y][x-1] if x > 0 else 100000
        scores[y].append(local + min(down_score, right_score))

# Do a further passes, this time account for other directions
path_total = scores[-1][-1]
while True:
    changes_needed = False
    for y in range(height):
        for x in range(width):
            local = grid[y][x]
            down_score = scores[y-1][x] if y > 0 else 100000
            right_score = scores[y][x-1] if x > 0 else 100000
            up_score = scores[y+1][x] if y < height - 1 else 100000
            left_score = scores[y][x+1] if x < width -1 else 100000
            new_score = min(
                scores[y][x],
                down_score + local,
                right_score + local,
                up_score + local,
                left_score + local,
            )
            if new_score != scores[y][x]:
                changes_needed = True
            scores[y][x] = new_score
    if path_total == scores[-1][-1] and not changes_needed:
        break
    path_total = scores[-1][-1]
    # print(f"{path_total}")

part_01 = scores[-1][-1] - scores[0][0]
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

def local_score(x : int, y : int) -> int:
    grid_y = y % len(grid)
    grid_x = x % len(grid[grid_y])
    score = grid[grid_y][grid_x]
    score += y // len(grid) + x // len(grid)
    if score > 9:
        score -= 9
    return score

width *= 5
height *= 5

scores = []
for y in range(height):
    scores.append([])
    for x in range(width):
        local = local_score(x, y)
        if x == 0 and y == 0:
            scores[y].append(0)
            continue
        down_score = scores[y-1][x] if y > 0 else 100000
        right_score = scores[y][x-1] if x > 0 else 100000
        scores[y].append(local + min(down_score, right_score))
    # print(f"{scores[y]}")

path_total = scores[-1][-1]
while True:
    changes_needed = False
    for y in range(height):
        for x in range(width):
            local = local_score(x, y)
            down_score = scores[y-1][x] if y > 0 else 100000
            right_score = scores[y][x-1] if x > 0 else 100000
            up_score = scores[y+1][x] if y < height - 1 else 100000
            left_score = scores[y][x+1] if x < height -1 else 100000
            new_score = min(
                scores[y][x],
                down_score + local,
                right_score + local,
                up_score + local,
                left_score + local,
            )
            if new_score != scores[y][x]:
                changes_needed = True
            scores[y][x] = new_score
    if path_total == scores[-1][-1] and not changes_needed:
        break
    path_total = scores[-1][-1]
    # print(f"{path_total}")


part_02 = scores[-1][-1]
print(f"Result: {part_02}")
