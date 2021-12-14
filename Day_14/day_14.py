#!/usr/bin/env python3


input_file = open("Day_14/input", "r")
# input_file = open("Day_14/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]

# Part 1
print("Part 1:")

polymer_template = list(lines[0])
insertions_list = [(line.split(" -> ")) for line in lines[2:]]
insertion_maps = {}
for insertion in insertions_list:
    first_element = insertion[0][0]
    second_element = insertion[0][1]
    insert = insertion[1]
    if first_element not in insertion_maps:
        insertion_maps[first_element] = {}
    insertion_maps[first_element][second_element] = insert


# print(f"{polymer_template}")
# print(f"{insertions_list}")
# print(f"{insertion_maps}")

polymer = list(polymer_template)
for step in range(10):
    new_polymer = []
    for e1, e2 in zip(polymer[:-1], polymer[1:]):
        new_polymer.append(e1)
        new_polymer.append(insertion_maps[e1][e2])
    new_polymer.append(polymer[-1])
    polymer = new_polymer
    # print(f"After step {step + 1}: {polymer}")

counts = {}
min_count = 9223372036854775807
max_count = 0
for key in insertion_maps:
    count = sum(1 for element in polymer if element == key)
    counts[key] = count
    min_count = min(counts[key], min_count)
    max_count = max(counts[key], max_count)

# print(f"{len(polymer)}, {counts}, {min_count}, {max_count}")

part_01 = max_count - min_count
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

# Need more efficient approach

polymer = list(polymer_template)
pair_counts = {}
for e1 in insertion_maps:
    pair_counts[e1] = {}
    for e2 in insertion_maps:
        pair_counts[e1][e2] = 0

for e1, e2 in zip(polymer[:-1], polymer[1:]):
    pair_counts[e1][e2] += 1

# print(f"{pair_counts}")

for step in range(40):
    new_pair_counts = {}
    for e1 in pair_counts:
        if e1 not in new_pair_counts:
            new_pair_counts[e1] = {}
        for e2 in pair_counts[e1]:
            ins = insertion_maps[e1][e2]

            # Does python have an autovivicating dict?
            if ins not in new_pair_counts:
                new_pair_counts[ins] = {}
            if ins not in new_pair_counts[e1]:
                new_pair_counts[e1][ins] = 0
            if e2 not in new_pair_counts[ins]:
                new_pair_counts[ins][e2] = 0

            new_pair_counts[e1][ins] += pair_counts[e1][e2]
            new_pair_counts[ins][e2] += pair_counts[e1][e2]
    pair_counts = new_pair_counts
    # print(f"{pair_counts}")


counts = {}
for key in pair_counts:
    counts[key] = sum(pair_counts[key].values())

# The last element for the original polymer will need to be counted once more
counts[polymer[-1]] += 1

min_count = min(counts.values())
max_count = max(counts.values())

# print(f"{counts}, {min_count}, {max_count}")

part_02 = max_count - min_count
print(f"Result: {part_02}")
