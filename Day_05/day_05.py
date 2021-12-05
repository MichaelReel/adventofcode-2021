#!/usr/bin/env python3


input_file = open("Day_05/input", "r")
lines = [x for x in input_file.readlines()]
# lines = [
#     "0,9 -> 5,9",
#     "8,0 -> 0,8",
#     "9,4 -> 3,4",
#     "2,2 -> 2,1",
#     "7,0 -> 7,4",
#     "6,4 -> 2,0",
#     "0,9 -> 2,9",
#     "3,4 -> 1,4",
#     "0,0 -> 8,8",
#     "5,5 -> 8,2",
# ]


class Vector:
    x : int
    y : int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def in_line_with(self, other: "Vector") -> bool:
        return self.x == other.x or self.y == other.y

    def grid_line_to(self, other: "Vector") -> list["Vector"]:
        if self.x == other.x:
            return self._vertical_line_to(other = other)
        elif self.y == other.y:
            return self._hortizontal_line_to(other = other)
    
    def ordinal_line_to(self, other: "Vector") -> list["Vector"]:
        if self.in_line_with(other = other):
            return self.grid_line_to(other = other)
        else:
            return self._diagonal_line_to(other = other)
    
    def _vertical_line_to(self, other: "Vector") -> list["Vector"]:
        vector_line : list[Vector] = []
        dy = 1 if other.y >= self.y else -1
        for y in range(self.y, other.y, dy):
            vector_line.append(Vector(self.x, y))
        vector_line.append(other)
        return vector_line
    
    def _hortizontal_line_to(self, other: "Vector") -> list["Vector"]:
        vector_line : list[Vector] = []
        dx = 1 if other.x >= self.x else -1
        for x in range(self.x, other.x, dx):
            vector_line.append(Vector(x, self.y))
        vector_line.append(other)
        return vector_line
    
    def _diagonal_line_to(self, other: "Vector") -> list["Vector"]:
        vector_line : list[Vector] = []
        dy = 1 if other.y >= self.y else -1
        dx = 1 if other.x >= self.x else -1
        y = self.y
        for x in range(self.x, other.x, dx):
            vector_line.append(Vector(x, y))
            y += dy
        vector_line.append(other)
        return vector_line



class OceanFloor:
    vent_data : list[list[int]]
    max_x : int
    max_y : int
    danger_vents : int

    def __init__(self) -> None:
        # Memory efficiency? What's that?
        self.vent_data = [[0 for i in range(1000)] for j in range(1000)]
        self.max_x = -1
        self.max_y = -1
        self.danger_vents = 0
    
    def __repr__(self) -> str:
        repr_str = ""
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                repr_str += f"{self.vent_data[y][x]}"
            repr_str += "\n"
        return repr_str

    def apply_vent_line(self, vent_line: list["Vector"]) -> None:
        for vent in vent_line:
            self.vent_data[vent.y][vent.x] += 1

            # Count as we go, only if we get to exactly 2 count it
            if self.vent_data[vent.y][vent.x] == 2:
                self.danger_vents += 1

            # Update values useful for the debug repr
            self.max_y = max(self.max_y, vent.y)
            self.max_x = max(self.max_x, vent.x)

            # print(f"{vent} = {self.vent_data[vent.y][vent.x]}")

    def count_danger_vents(self) -> int:
        return self.danger_vents

        # # Below is the Super-not efficient way to do this
        # # but this is what I used for the initial results and was surprisingly quick:

        # danger_vents = 0
        # for y in range(self.max_y + 1):
        #     for x in range(self.max_x + 1):
        #         if self.vent_data[y][x] >= 2:
        #             danger_vents += 1
        # return danger_vents



# Part 1
print("Part 1:")

# data set has no negative values or values above 999
ocean_floor = OceanFloor()

for line in lines:
    start_str, end_str = line.split(" -> ")
    start = Vector(*[int(coord) for coord in start_str.split(",")])
    end = Vector(*[int(coord) for coord in end_str.split(",")])
    # print(f"{start} -> {end}")
    
    if start.in_line_with(other = end):
        vent_line = start.grid_line_to(other = end)
        ocean_floor.apply_vent_line(vent_line = vent_line)
        # print(f"{vent_line}")

# print(f"{ocean_floor}")

part_01 = ocean_floor.count_danger_vents()
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

ocean_floor = OceanFloor()

for line in lines:
    start_str, end_str = line.split(" -> ")
    start = Vector(*[int(coord) for coord in start_str.split(",")])
    end = Vector(*[int(coord) for coord in end_str.split(",")])

    vent_line = start.ordinal_line_to(other = end)
    ocean_floor.apply_vent_line(vent_line = vent_line)
    # print(f"{vent_line}")

# print(f"{ocean_floor}")

part_02 = ocean_floor.count_danger_vents()
print(f"Result: {part_02}")
