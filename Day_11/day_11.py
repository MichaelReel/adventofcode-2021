#!/usr/bin/env python3


input_file = open("Day_11/input", "r")
# input_file = open("Day_11/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]


def raise_energy(octopii: list[list[int]], flashes: list[list[int]], x:int, y:int) -> None:
    if (x < 0 or x > 9):
        print(f"{x}, {y}")
    if (y < 0 or y > 9):
        print(f"{x}, {y}")
    if flashes[y][x] == 0:
        octopii[y][x] += 1
        if octopii[y][x] > 9:
            flashes[y][x] = 1
            for ny in range(max(0,y-1), min(10,y+2)):
                for nx in range(max(0,x-1), min(10,x+2)):
                    raise_energy(octopii, flashes, nx, ny)
            octopii[y][x] = 0


# Part 1
print("Part 1:")

octopii = [[int(x) for x in line] for line in lines]
total_flashes = 0
for step in range(100):
    flashes = [[0]*10 for _i in range(10)]
    for octo_index in range(100):
        y = octo_index // 10
        x = octo_index % 10
        raise_energy(octopii, flashes, x, y)
    flash_count = sum(sum(flashes, []))
    # print(f"{flash_count}")
    total_flashes += flash_count
# print(f"{octopii}")

part_01 = total_flashes
print(f"Result: {part_01}")


# Part 2
print("Part 2:")
octopii = [[int(x) for x in line] for line in lines]

step = 0
sync = False
while not sync:
    step += 1
    flashes = [[0]*10 for _i in range(10)]
    for octo_index in range(100):
        y = octo_index // 10
        x = octo_index % 10
        raise_energy(octopii, flashes, x, y)
    flash_count = sum(sum(flashes, []))
    if flash_count == 100:
        sync = True

part_02 = step
print(f"Result: {part_02}")
