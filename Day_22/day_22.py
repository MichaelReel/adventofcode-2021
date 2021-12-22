#!/usr/bin/env python3
from collections import namedtuple
import collections
from re import match


input_file = open("Day_22/input", "r")
# input_file = open("Day_22/sample_input", "r")
# input_file = open("Day_22/sample_input_2", "r")
lines = [x.strip() for x in input_file.readlines()]


# Part 1
print("Part 1:")

class Vector(namedtuple("Vector", "x y z")):
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


class AABB(namedtuple("AABB", "start end")):
    def __repr__(self) -> str:
        return f"{self.start} -> {self.end}"
    
    def size(self) -> int:
        return (1 + self.end.x - self.start.x) * (1 + self.end.y - self.start.y) * (1 + self.end.z - self.start.z)
    
    def overlap(self, other: "AABB") -> "AABB":
        start = Vector(max(self.start.x, other.start.x), max(self.start.y, other.start.y), max(self.start.z, other.start.z))
        end = Vector(min(self.end.x, other.end.x), min(self.end.y, other.end.y), min(self.end.z, other.end.z))
        overlap_aabb = None
        if start.x <= end.x and start.y <= end.y and start.z <= end.z:
            overlap_aabb = AABB(start, end)
        return overlap_aabb


class Instruction(namedtuple("Instruction", "step area")):
    def __repr__(self) -> str:
        repr_str = "[ on]" if self.step else "[off]"
        repr_str += f": {self.area}"
        return repr_str
    
    def overlaps_or_in_range(self) -> bool:
        if self.area.end.x < -50 or self.area.start.x > 50:
            return False
        if self.area.end.y < -50 or self.area.start.y > 50:
            return False
        if self.area.end.z < -50 or self.area.start.z > 50:
            return False
        return True


class Grid(dict):
    def __init__(self) -> None:
        for x in range(-50, 51):
            y_dict = {}
            for y in range(-50, 51):
                z_dict = {}
                for z in range(-50, 51):
                    z_dict[z] = False
                y_dict[y] = z_dict
            self[x] = y_dict
    
    def apply_instruction(self, inst: Instruction) -> None:
        for x in range(inst.area.start.x, inst.area.end.x + 1):
            for y in range(inst.area.start.y, inst.area.end.y + 1):
                for z in range(inst.area.start.z, inst.area.end.z + 1):
                    self[x][y][z] = inst.step

    def get_count(self) -> int:
        total = 0
        for x in range(-50, 51):
            for y in range(-50, 51):
                for z in range(-50, 51):
                    total += 1 if self[x][y][z] else 0
        return total


instructions = []
for line in lines:
    step_re = r"(?P<step>\w+)"
    x_re = r"x=(?P<x_a>-?\d+)\.\.(?P<x_b>-?\d+)"
    y_re = r"y=(?P<y_a>-?\d+)\.\.(?P<y_b>-?\d+)"
    z_re = r"z=(?P<z_a>-?\d+)\.\.(?P<z_b>-?\d+)"
    inst = match(r"^" + step_re + r" " + x_re + r"," + y_re + r"," + z_re + r"$", line).groupdict()
    start_vector = Vector( int(inst["x_a"]), int(inst["y_a"]), int(inst["z_a"]) )
    end_vector = Vector( int(inst["x_b"]), int(inst["y_b"]), int(inst["z_b"]) )
    area = AABB(start_vector, end_vector)
    step = True if inst["step"] == "on" else False
    instructions.append(Instruction(step, area))


# Create grid (not convinced this is the best way):
grid = Grid()
for inst in instructions:
    if inst.overlaps_or_in_range():
        grid.apply_instruction(inst)

part_01 = grid.get_count()
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

# There's no way the grid thing will work for the bigger inputs.
# Another approach is to get each instructions grid size
# Find the overlaps in "ons" and ignore one side
# Find the overlaps in "offs" and remove from previous

class OverlapInstruction():
    id: str
    step: bool
    area: AABB
    collisions: list["OverlapInstruction"]

    def __init__(self, id: str, step: bool, area: AABB) -> None:
        self.id = id
        self.step = step
        self.area = area
        self.collisions = []

    def __repr__(self) -> str:
        repr_str = f"{self.id} "
        repr_str += "[ on]" if self.step else "[off]"
        repr_str += f": {self.area}"
        repr_str += f", {self.area.size()}"
        return repr_str
    
    def overlap(self, other: "OverlapInstruction") -> AABB:
        return self.area.overlap(other.area)
    
    def push_down_overlaps(self) -> None:
        reference_space = []
        while self.collisions:
            inst = self.collisions.pop(0)
            for other_inst in reference_space:
                overlap_area = inst.overlap(other_inst)
                if overlap_area:
                    sub_inst = OverlapInstruction(f"({other_inst.id}):{inst.id}", inst.step, overlap_area)
                    other_inst.collisions.append(sub_inst)
            reference_space.append(inst)
        
        for inst in reference_space:
            inst.push_down_overlaps()
        
        self.collisions = reference_space
    
    def get_total_applied_count(self) -> int:
        count = self.area.size()
        # Apply collisions in order to figure out the total count
        for inst in self.collisions:
            sub_count = inst.get_total_applied_count()
            count -= sub_count
        # print(f"Calculating: {self}, Got: {count}")
        return count


reference_space = []
overlap_instructions = [OverlapInstruction(str(i), inst.step, inst.area) for i, inst in enumerate(instructions)]
while overlap_instructions:
    inst = overlap_instructions.pop(0)
    # Go through each instruction and apply it to a reference space
    for other_inst in reference_space:
        overlap_area = inst.overlap(other_inst)
        if overlap_area:
            sub_inst = OverlapInstruction(f"({other_inst.id}):{inst.id}", inst.step, overlap_area)
            other_inst.collisions.append(sub_inst)
    reference_space.append(inst)

# reference space now has each instruction plus all the overlapping areas that will apply to this area
for inst in reference_space:
    # For each space, give it's own reference space
    inst.push_down_overlaps()

# Now all the overlaps are nested, we should try to get each areas score with the overlaps accounted for
# The last instruction will apply directly as it will not be overwritten, where other areas are overwritten they should try to account for this
total_count = 0

for inst in reference_space:
    count = inst.get_total_applied_count()
    # print(f"{inst.id} : {count}")
    if inst.step:
        total_count += count

part_02 = total_count
print(f"Result: {part_02}")
