#!/usr/bin/env python3
from collections import namedtuple
from typing import Optional, Union


input_file = open("Day_24/input", "r")
lines = [x.strip() for x in input_file.readlines()]


class Instruction(namedtuple("Instruction", "operator variable value")):
    def __repr__(self) -> str:
        return f"{self.operator} {self.variable} {self.value}"


# Grab input blocks
instructions = []
for line in lines:
    tokens = line.split(' ')
    value = (tokens[2:3] or (None,))[0]
    if value not in [None, "w", "x", "y", "z"]:
        value = int(value)
    instructions.append(Instruction(tokens[0],tokens[1],value))

inst_blocks = []
while instructions:
    instruction = instructions.pop(0)
    if instruction.operator == "inp":
        inst_blocks.append([])
    else:
        inst_blocks[-1].append(instruction)

for block in inst_blocks:
    print(f"{block}")


# Define the APU we'll use to process each block of instructions
class ALU:
    def __init__(self, program : list[Instruction]) -> None:
        self.program = program
        self.mem = { 'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0 }
    
    def build_program_expression(self, w: int, x: int = 0, y: int = 0, z: int = 0) -> dict[str, int]:
        self.mem = { 'w' : w, 'x' : x, 'y' : y, 'z' : z }
        for ins in self.program:
            if ins.operator == "add":
                self.mem[ins.variable] = self._add(ins)
            elif ins.operator == "mul":
                self.mem[ins.variable] = self._mul(ins)
            elif ins.operator == "div":
                self.mem[ins.variable] = self._div(ins)
            elif ins.operator == "mod":
                self.mem[ins.variable] = self._mod(ins)
            elif ins.operator == "eql":
                self.mem[ins.variable] = self._eql(ins)
        return self.mem["w"], self.mem["x"], self.mem["y"], self.mem["z"]

    def _add(self, ins: Instruction) -> Union[Instruction, int]:
        a = self._get_a(ins)
        b = self._get_b(ins)
        if isinstance(a, int) and isinstance(b, int):
            return a + b
        elif b == 0:
            return a
        elif a == 0:
            return b
        return ins

    def _mul(self, ins: Instruction) -> Union[Instruction, int]:
        a = self._get_a(ins)
        b = self._get_b(ins)
        if isinstance(a, int) and isinstance(b, int):
            return a * b
        elif a == 0 or b == 0:
            return 0
        elif a == 1:
            return b
        elif b == 1:
            return a
        return ins

    def _div(self, ins: Instruction) -> Union[Instruction, int]:
        a = self._get_a(ins)
        b = self._get_b(ins)
        if isinstance(a, int) and isinstance(b, int):
            return a // b
        elif a == 0:
            return 0
        elif b == 1:
            return a
        return ins

    def _mod(self, ins: Instruction) -> Union[Instruction, int]:
        a = self._get_a(ins)
        b = self._get_b(ins)
        if isinstance(a, int) and isinstance(b, int):
            return a % b
        elif a == 0:
            return 0
        elif b == 1:
            return 0
        return ins

    def _eql(self, ins: Instruction) -> Union[Instruction, int]:
        a = self._get_a(ins)
        b = self._get_b(ins)
        if isinstance(a, int) and isinstance(b, int):
            return 1 if a == b else 0
        elif b == 0 and isinstance(a, Instruction) and a.operator == "eql":
            return Instruction("neq", a.variable, a.value)
        elif b == 1 and isinstance(a, Instruction) and a.operator == "eql":
            return a
        return ins

    def _get_a(self, ins : Instruction) -> Union[Instruction, int]:
        return self.mem[ins.variable]
    
    def _get_b(self, ins : Instruction) -> Union[Instruction, int]:
        return ins.value if not ins.value in self.mem else self.mem[ins.value]


def find_negative_add_to_x_instruction(block : list[Instruction]) -> Optional[int]:
    # This finds the values to make the inner condition false
    # This is used to prevent the z expression from growing
    # Cheers Reddit!
    for ins in block:
        if ins.operator == "add" and ins.variable == "x" and isinstance(ins.value, int):
            return ins.value if ins.value < 0 else None
    return None


# Part 1
print("Part 1:")

# Setup starting inputs - Input is only ever put into the w space
# We've dropped the inp instructions so we'll just load the input straight into w
results = {}
alu = ALU(inst_blocks[0])
for w in range(9, 0 ,-1):
    _, x, y, z = alu.build_program_expression(w, 0, 0, 0)
    results[z] = [w]  # Z should be 9 to 17
print(f"Step 0 w={w} z={min(results)}..{max(results)} {len(results)}")


for i, block in enumerate(inst_blocks[1:], start=1):
    prev_results = results
    results = {}
    neg_to_x = find_negative_add_to_x_instruction(block)
    alu = ALU(block)
    for w in range(9, 0 ,-1):
        for z in prev_results:
            if neg_to_x and ((z % 26) + neg_to_x != w):
                # Optimisation touted on reddit - can't take credit for this one!
                continue
            _, x, y, new_z = alu.build_program_expression(w, 0, 0, z)
            if new_z not in results:
                results[new_z] = prev_results[z] + [w]
    print(f"Step 0 w={w} z={min(results)}..{max(results)} {len(results)}")

# The results should have a 0 for z
part_01 = "".join(str(x) for x in results[0])
print(f"Result: {part_01}")


# Part 2
print("Part 2:")

alu = ALU(inst_blocks[0])
for w in range(1, 10):
    _, x, y, z = alu.build_program_expression(w, 0, 0, 0)
    results[z] = [w]  # Z should be 9 to 17
print(f"Step 0 w={w} z={min(results)}..{max(results)} {len(results)}")


for i, block in enumerate(inst_blocks[1:], start=1):
    prev_results = results
    results = {}
    neg_to_x = find_negative_add_to_x_instruction(block)
    alu = ALU(block)
    for w in range(1, 10):
        for z in prev_results:
            if neg_to_x and ((z % 26) + neg_to_x != w):
                # Optimisation touted on reddit - can't take credit for this one!
                continue
            _, x, y, new_z = alu.build_program_expression(w, 0, 0, z)
            if new_z not in results:
                results[new_z] = prev_results[z] + [w]
    print(f"Step 0 w={w} z={min(results)}..{max(results)} {len(results)}")

part_02 = "".join(str(x) for x in results[0])
print(f"Result: {part_02}")