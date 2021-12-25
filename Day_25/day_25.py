#!/usr/bin/env python3


input_file = open("Day_25/input", "r")
# input_file = open("Day_25/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]

# Part 1
print("Part 1:")
next_state = lines

print(f"Initial state:")
for line in next_state:
    print(f"{line}")

height = len(lines)
width = len(lines[0])
move = True
count = 0
while move:
    prev_state = next_state
    next_state = []
    move = False
    for y in range(height):
        new_line = []
        for x in range(width):
            if prev_state[y][x] == ".":
                if prev_state[y][x - 1] == ">":
                    new_line.append(">")
                    move = True
                elif prev_state[y -1][x] == "v":
                    new_line.append("v")
                    move = True
                else:
                    new_line.append(".")
            elif prev_state[y][x] == ">":
                if prev_state[y][(x + 1) % width] == ".":
                    if prev_state[y - 1][x] == "v":
                        new_line.append("v")
                        move = True
                    else:
                        new_line.append(".")
                        move = True
                else:
                    new_line.append(">")
            elif prev_state[y][x] == "v":
                if prev_state[(y + 1) % height][x] == "." and prev_state[(y + 1) % height][x - 1] != ">":
                    new_line.append(".")
                    move = True
                elif prev_state[(y + 1) % height][x] == ">" and prev_state[(y + 1) % height][(x + 1) % width] == ".":
                    new_line.append(".")
                    move = True
                else:
                    new_line.append("v")
        next_state.append(new_line)
    count += 1

    print(f"\nAfter {count} steps:")
    for line in next_state:
        print(f"{''.join(line)}")


part_01 = count
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

part_02 = "not implemented yet"
print(f"Result: {part_02}")
