#!/usr/bin/env python3


input_file = open("Day_03/input", "r")
lines = [x.strip() for x in input_file.readlines()]

# lines = [
#     "00100",
#     "11110",
#     "10110",
#     "10111",
#     "10101",
#     "01111",
#     "00111",
#     "11100",
#     "10000",
#     "11001",
#     "00010",
#     "01010",
# ]

# Part 1
print("Part 1:")

binary_positions = [0] * len(lines[0])
for line in lines:
    binary_positions = [bin + int(lin, 2) for bin, lin in zip(binary_positions, list(line))]

line_count = len(lines)
inverse_values = [line_count - bin for bin in binary_positions]

gamma_bin = ""
epsilon_bin = ""
for i in range(len(binary_positions)):
    if binary_positions[i] > inverse_values[i]:
        gamma_bin += "1"
        epsilon_bin += "0"
    else:
        gamma_bin += "0"
        epsilon_bin += "1"
gamma = int(gamma_bin, 2)
epsilon = int(epsilon_bin, 2)

part_01 = gamma * epsilon
print(f"Result: {part_01}")

# Part 2
print("Part 2:")
oxygen_lines = list(lines)
for bit_i in range(len(oxygen_lines[0])):
    # consider the current bit of the remaining data points
    bin = sum([int(line[bit_i],2) for line in oxygen_lines])

    # Keep the lines that match the greater number of bit in this position
    filter = "1" if bin >= (len(oxygen_lines) - bin) else "0"
    oxygen_lines = [line for line in oxygen_lines if line[bit_i] == filter]

    if len(oxygen_lines) == 1:
        break

carbon_lines = list(lines)
for bit_i in range(len(carbon_lines[0])):
    # consider the current bit of the remaining data points
    bin = sum([int(line[bit_i],2) for line in carbon_lines])

    # Keep the lines that match the fewer number of bits in this position
    filter = "1" if bin < (len(carbon_lines) - bin) else "0"
    carbon_lines = [line for line in carbon_lines if line[bit_i] == filter]

    if len(carbon_lines) == 1:
        break

oxygen = int(oxygen_lines[0], 2)
carbon = int(carbon_lines[0], 2)

part_02 = oxygen * carbon
print(f"Result: {part_02}")
