#!/usr/bin/env python3


input_file = open("Day_10/input", "r")
# input_file = open("Day_10/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]

# Part 1
print("Part 1:")

# Naive chunk type counter
chunk_closer = {")": "(", "]": "[", "}": "{", ">": "<"}
chunk_error_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}

failure_score = 0
for line in lines:
    chunk_stack = []
    for char in line:
        if char in chunk_closer:
            current_open = chunk_stack.pop()
            if current_open != chunk_closer[char]:
                failure_score += chunk_error_scores[char]
        else:
            chunk_stack.append(char)
        

part_01 = failure_score
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

# Naive chunk type counter
chunk_closer = {")": "(", "]": "[", "}": "{", ">": "<"}
chunk_closer_scores = {"(": 1, "[": 2, "{": 3, "<": 4}

scores = []
for line in lines:
    keep = True
    chunk_stack = []
    for char in line:
        if char in chunk_closer:
            current_open = chunk_stack.pop()
            if current_open != chunk_closer[char]:
                keep = False
                break
        else:
            chunk_stack.append(char)
    if keep:
        # print(f"valid line: {line}")
        # print(f"remaining stack: {chunk_stack}")
        score = 0
        while chunk_stack:
            score *= 5
            score += chunk_closer_scores[chunk_stack.pop()]
        scores.append(score)
        # print(f"score: {score}")

scores = sorted(scores)

part_02 = scores[len(scores) // 2]
print(f"Result: {part_02}")
