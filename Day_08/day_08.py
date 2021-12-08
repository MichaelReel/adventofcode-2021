#!/usr/bin/env python3


input_file = open("Day_08/input", "r")
# input_file = open("Day_08/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]
# lines = ["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"]

# Part 1
print("Part 1:")

easy_digits = 0
for line in lines:
    signal_patterns, output_value = [part.split(" ") for part in line.split(" | ")]
    easy_digits += len([digit for digit in output_value if (len(digit) in [2,4,3,7])])

part_01 = easy_digits
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

# Let's go naive approach!

total_decoded_values = 0
for line in lines:
    pattern_table = {2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
    value_mappings = [None] * 10
    segment_counts = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0}
    segment_maps = {"a": None, "b": None, "c": None, "d": None, "e": None, "f": None, "g": None}

    signal_patterns, output_value = [part.split(" ") for part in line.split(" | ")]

    # Map lengths to patterns
    for pattern in signal_patterns:
        pattern_table[len(pattern)].append(pattern)
        for segment in pattern:
            segment_counts[segment] += 1

    # Map the digits we know by counts
    for k, v in segment_counts.items():
        if v == 4:
            segment_maps["e"] = k
        if v == 6:
            segment_maps["b"] = k
        if v == 9:
            segment_maps["f"] = k

    # Map the 4 value mappings we know by length
    value_mappings[1] = pattern_table[2][0]
    value_mappings[4] = pattern_table[4][0]
    value_mappings[7] = pattern_table[3][0]
    value_mappings[8] = pattern_table[7][0]

    # We know f is in 1, so the other value is c
    segment_maps["c"] = value_mappings[1].replace(segment_maps["f"], "")
    # f and c are in 7, the other value is a
    segment_maps["a"] = value_mappings[7].replace(segment_maps["f"], "").replace(segment_maps["c"], "")
    # b, c, f are in 4, the other value is d
    segment_maps["d"] = value_mappings[4].replace(segment_maps["b"], "").replace(segment_maps["f"], "").replace(segment_maps["c"], "")
    # g is whatever is left
    segment_maps["g"] = value_mappings[8].replace(segment_maps["a"], "").replace(segment_maps["b"], "").replace(segment_maps["c"], "").replace(segment_maps["d"], "").replace(segment_maps["e"], "").replace(segment_maps["f"], "")

    # Have all segment mappings now get other value_mappings
    for pattern in pattern_table[5]:
        if segment_maps["e"] in pattern:
            value_mappings[2] = pattern
        elif segment_maps["b"] in pattern:
            value_mappings[5] = pattern
        else:
            value_mappings[3] = pattern
    for pattern in pattern_table[6]:
        if segment_maps["d"] not in pattern:
            value_mappings[0] = pattern
        elif segment_maps["c"] not in pattern:
            value_mappings[6] = pattern
        elif segment_maps["e"] not in pattern:
            value_mappings[9] = pattern
    
    # Invert value mappings - sort the patterns
    pattern_mappings = {"".join(sorted(k)):str(v) for v, k in enumerate(value_mappings)}

    # Sort each output value's digit and convert to a number
    decimal_str = ""
    for digit in output_value:
        decimal_str += pattern_mappings["".join(sorted(digit))]
    
    total_decoded_values += int(decimal_str)


part_02 = total_decoded_values
print(f"Result: {part_02}")
