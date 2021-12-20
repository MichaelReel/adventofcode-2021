#!/usr/bin/env python3


input_file = open("Day_20/input", "r")
# input_file = open("Day_20/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]

# Create a map from the map block to the result:
block_to_pixel = {}
for i, char in enumerate(lines[0]):
    key = f"{i:>09b}".replace("0",".").replace("1","#")
    block_to_pixel[key] = char

# for key,value in block_to_pixel.items():
#     print(f"{key} -> {value}")

# Expand input are before parsing
def expand_area(original: list[str], fill_char: str = ".", padding: int = 2) -> list[str]:
    expanded = []
    for _ in range(padding):
        expanded.append(fill_char * (len(original[0]) + (padding * 2)))
    for line in original:
        expanded.append((fill_char * padding) + line + (fill_char * padding))
    for _ in range(padding):
        expanded.append(fill_char * (len(original[0]) + (padding * 2)))
    return expanded


# Get the block string for the current point
def get_block(area: list[str], x: int, y: int) -> str:
    block = ""
    for dy in range(-1,2):
        for dx in range(-1,2):
            block += area[y + dy][x + dx]
    return block


# Parse each block and insert into output
def apply_mappings(input_area: list[str]) -> list[str]:
    output_area = []
    for y in range(1,len(input_area) - 1):
        new_line = ""
        for x in range(1,len(input_area[y]) - 1):
            block = get_block(input_area, x, y)
            pixel = block_to_pixel[block]
            # print(f"{block} maps to {pixel} for ({x},{y})")
            new_line += block_to_pixel[block]
        output_area.append(new_line)
    return output_area


# Part 1
print("Part 1:")

# Parse input
input_area = expand_area(lines[2:])

# Apply mappings once
output_area = apply_mappings(input_area)

# Apply mappings a second time (fill with the 0 char this time, as that'll be how the (infinity) is filled)
input_area = expand_area(output_area, fill_char=block_to_pixel["........."])
output_area = apply_mappings(input_area)

# Count "#"s
part_01 = "".join(output_area).count("#")
print(f"Result: {part_01}")


# Part 2
print("Part 2:")

# Parse input
output_area = lines[2:]

odd_fill = block_to_pixel["........."]
even_fill = block_to_pixel[odd_fill * 9]

# print(f"odd_fill : \"{odd_fill}\", even_fill : \"{even_fill}\"")

for i in range(50):
    fill_char = even_fill if i % 2 == 0 else odd_fill
    if i == 0:
        fill_char = "."
    input_area = expand_area(output_area, fill_char=fill_char)
    output_area = apply_mappings(input_area)
    # print(f"Mappings applied {i+1} times")

part_02 = "".join(output_area).count("#")
print(f"Result: {part_02}")
