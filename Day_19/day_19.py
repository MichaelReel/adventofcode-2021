#!/usr/bin/env python3
from collections import namedtuple
from itertools import product
from re import match


input_file = open("Day_19/input", "r")
# input_file = open("Day_19/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]


class Point(namedtuple("Point", "x y z")):

    def add(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def multiply(self, other: "Point") -> "Point":
        return Point(self.x * other.x, self.y * other.y, self.z * other.z)

    def size(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)
    
    def _value(self) -> int:
        """Assuming only one of these has an actual value: """
        return self.x + self.y + self.z

    def rotate(self, matrix: list["Point"]) -> "Point":
        parts = [self.multiply(m)._value() for m in matrix]
        return Point(*parts)

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z})"


pm = {
    " x": Point(1, 0, 0),
    "-x": Point(-1, 0, 0),
    " y": Point(0, 1, 0),
    "-y": Point(0, -1, 0),
    " z": Point(0, 0, 1),
    "-z": Point(0, 0, -1),
}


orientation_map = [
    [pm[" x"],pm[" y"],pm[" z"]], # 0, 0, 0
    [pm[" x"],pm["-y"],pm["-z"]], # 0, 180, 180
    [pm[" x"],pm[" z"],pm["-y"]], # 90, 0, 0
    [pm[" x"],pm["-z"],pm[" y"]], # 270, 0, 0

    [pm["-x"],pm[" y"],pm["-z"]], # 0, 180, 0
    [pm["-x"],pm["-y"],pm[" z"]], # 0, 0, 180
    [pm["-x"],pm[" z"],pm[" y"]], # 270, 0, 180
    [pm["-x"],pm["-z"],pm["-y"]], # 90, 0, 180

    [pm[" y"],pm[" x"],pm["-z"]], # 0, 180, 90
    [pm[" y"],pm["-x"],pm[" z"]], # 0, 0, 90
    [pm[" y"],pm[" z"],pm[" x"]], # 0, 90, 90
    [pm[" y"],pm["-z"],pm["-x"]], # 0, 270, 90

    [pm["-y"],pm[" x"],pm[" z"]], # 0, 0, 270
    [pm["-y"],pm["-x"],pm["-z"]], # 0, 180, 270
    [pm["-y"],pm[" z"],pm["-x"]], # 0, 270, 270
    [pm["-y"],pm["-z"],pm[" x"]], # 0, 90, 270

    [pm[" z"],pm[" x"],pm[" y"]], # 270, 0, 270
    [pm[" z"],pm["-x"],pm["-y"]], # 90, 0, 90
    [pm[" z"],pm[" y"],pm["-x"]], # 0, 270, 0
    [pm[" z"],pm["-y"],pm[" x"]], # 0, 90, 180

    [pm["-z"],pm[" x"],pm["-y"]], # 90, 0, 270
    [pm["-z"],pm["-x"],pm[" y"]], # 270, 0, 90
    [pm["-z"],pm[" y"],pm[" x"]], # 0, 90, 0
    [pm["-z"],pm["-y"],pm["-x"]], # 0, 270, 180
]


class Scanner(list[Point]):
    id: str
    orientations : list["Scanner"] = None

    def __init__(self, id : str):
        self.id = id
    
    def get_orientations(self) -> list["Scanner"]:
        self.recreate_orientations()
        return self.orientations

    def recreate_orientations(self) -> None:
        self.orientations = []
        new_id = 0
        for orientation in orientation_map:
            oriented_scanner = Scanner(self.id + ":" + str(new_id))
            # print(f"{self.id}:{orientation}")
            for beacon in self:
                rotated = beacon.rotate(orientation)
                oriented_scanner.append(rotated)
                # print(f"    {rotated}")
            self.orientations.append(oriented_scanner)
            new_id = new_id + 1
    
    def align_first_to(self, point: Point) -> "Scanner":
        dxyz = point.subtract(self[0])
        return self.align_all_by(dxyz)
    
    def align_all_by(self, dxyz: Point) -> "Scanner":
        aligned_scanner = Scanner(self.id + " -> " + f"{dxyz}")
        for beacon in self:
            aligned_scanner.append(beacon.add(dxyz))
        return aligned_scanner

    def get_matches(self, other: "Scanner") -> list[Point]:
        return list(set(self).intersection(other))
    
    def get_mismatches(self, other: "Scanner") -> list[Point]:
        return list(set(self).difference(other))
    
    def __repr__(self) -> str:
        repr_str = f"--- scanner {self.id} ---\n"
        for beacon in self:
            repr_str += f"{beacon}\n"
        return repr_str


scanners : list[Scanner] = []

for line in lines:
    if scanner_match := match(r"^--- scanner (?P<id>-?\d+) ---$", line):
        scanner_line = scanner_match.groupdict()
        scanners.append(Scanner(scanner_line["id"]))
    elif point_match := match(r"^(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)$", line):
        point_line = point_match.groupdict()
        scanners[-1].append(Point(int(point_line["x"]), int(point_line["y"]), int(point_line["z"])))
    elif line == "":
        # Pre-load the orientations
        scanners[-1].get_orientations()

# Line everything up with first scanner
reference_scanner = scanners.pop(0)
beacon_offsets = [Point(0,0,0)]

# Try to align and merge each scanner into the reference
while scanners:
    # Take the first scanner, make each orientation, see if we can get 12 alignments
    test_scanner = scanners.pop(0)
    orientations = test_scanner.get_orientations()
    orientation_matched = False

    # Align the first value in orientation against each value in the reference scanner
    for orientation in orientations:
        # print(f"Trying orientation {orientation.id}")
        all_alignments = [a.subtract(b) for a,b in product(reference_scanner, orientation)]
        for beacon in all_alignments:
            aligned_scanner = orientation.align_all_by(beacon)
            matching_beacons = aligned_scanner.get_matches(reference_scanner)
            # If we get enough matches, merge into the refence and move onto the next scanner
            if len(matching_beacons) >= 12:
                # Kept this output, just to indicate it's still calculating:
                print(f"matches found!: {aligned_scanner.id}")

                for new_beacon in aligned_scanner.get_mismatches(reference_scanner):
                    reference_scanner.append(new_beacon)
                reference_scanner.recreate_orientations()
                orientation_matched = True
                beacon_offsets.append(beacon)
                break
        
        if orientation_matched:
            break
    
    if not orientation_matched:
        # If we don't get a match yet, pop scanner back on the end of the test queue
        scanners.append(test_scanner)

# Part 1
print("Part 1:")

part_01 = len(reference_scanner)
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

all_distances = [a.subtract(b).size() for a,b in product(beacon_offsets, beacon_offsets)]

part_02 = max(all_distances)
print(f"Result: {part_02}")
