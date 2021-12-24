#!/usr/bin/env python3
from collections import namedtuple


input_file = open("Day_24/input", "r")
lines = [x.strip() for x in input_file.readlines()]

Instruction = namedtuple("Instruction", "operator variable value")


class ALU:
    # mem : dict[str, int]
    # program : list[Instruction]
    input_cache : dict[str, dict[str, int]] = {
        "" : {
            'w' : 0,
            'x' : 0,
            'y' : 0,
            'z' : 0,
            'p' : 0,
        }
    }

    def __init__(self, program : list[Instruction]) -> None:
        self.mem = {
            'w' : 0,
            'x' : 0,
            'y' : 0,
            'z' : 0,
            'p' : 0,
        }
        self.program = program
    
    def run_program(self, input_buffer : list[int]) -> dict[str, int]:
        # Determine from the cache what point we can jump to in the instructions
        buffer_history = self._get_state_from_cache(input_buffer)

        # print(f"Running program against input {input_buffer}")
        for ins in self.program[self.mem['p']:]:
            # print(f"Preforming instruction {ins}")
            if ins.operator == "inp":
                self._inp(ins.variable, input_buffer, buffer_history)
            elif ins.operator == "add":
                self._add(ins.variable, ins.value)
            elif ins.operator == "mul":
                self._mul(ins.variable, ins.value)
            elif ins.operator == "div":
                self._div(ins.variable, ins.value)
            elif ins.operator == "mod":
                self._mod(ins.variable, ins.value)
            elif ins.operator == "eql":
                self._eql(ins.variable, ins.value)
            self.mem['p'] += 1

        return self.mem
    
    def _get_state_from_cache(self, buffer : list[int]) -> None:
        buffer_history = []

        # Find our best key:
        key = "".join(str(x) for x in buffer_history)
        while key in ALU.input_cache.keys():
            buffer_history.append(buffer.pop(0))
            key = "".join(str(x) for x in buffer_history)
        # Roll back to the to found state
        buffer.insert(0, buffer_history.pop())
        key = "".join(str(x) for x in buffer_history)
        self.mem = ALU.input_cache[key]

        return buffer_history
    
    def _inp(self, store, buffer, buffer_history) -> None:
        # Before reading the next value
        # cache the current process so we can get back to here more quickly
        key = "".join(str(x) for x in buffer_history)
        ALU.input_cache[key] = self.mem

        # Read the next value
        value = buffer.pop(0)
        self.mem[store] = value
        buffer_history.append(value)

    def _add(self, store, value_str) -> None:
        value = self._get_value(value_str)
        self.mem[store] += value
    
    def _mul(self, store, value_str) -> None:
        value = self._get_value(value_str)
        self.mem[store] *= value

    def _div(self, store, value_str) -> None:
        value = self._get_value(value_str)
        self.mem[store] //= value

    def _mod(self, store, value_str) -> None:
        value = self._get_value(value_str)
        self.mem[store] %= value

    def _eql(self, store, value_str) -> None:
        value = self._get_value(value_str)
        self.mem[store] = 1 if self.mem[store] == value else 0
    
    def _get_value(self, value_str) -> None:
        if value_str in self.mem:
            return self.mem[value_str]
        return int(value_str)





# Part 1
print("Part 1:")

instructions = []
for line in lines:
    tokens = line.split(' ')
    value = (tokens[2:3] or (None,))[0]
    instructions.append(Instruction(tokens[0],tokens[1],value))

# The brute force approach is just far too slow. We might want to work backwars through the instructions to find the correct

# alu = ALU(instructions)
# input_buffer = [9] * 14

# def decrement_buffer(input_buffer : list[int]):
#     digit = 13
#     while True:
#         input_buffer[digit] -= 1
#         if input_buffer[digit] == 0:
#             input_buffer[digit] = 9
#             digit -= 1
#         else:
#             break

#     return input_buffer

# tests = 0
# while True:

#     results = alu.run_program(input_buffer.copy())

#     # print(f"{ALU.input_cache}")
#     tests += 1
#     if tests % 10000 == 0:
#         print(f"{tests} tests: {''.join(str(x) for x in input_buffer)}")

#     if results['z'] == 0:
#         print(f"Model number found: {''.join(input_buffer)}")
#         break
    
#     input_buffer = decrement_buffer(input_buffer)


part_01 = "not implemented yet"
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

part_02 = "not implemented yet"
print(f"Result: {part_02}")
