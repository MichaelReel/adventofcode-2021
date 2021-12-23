#!/usr/bin/env python3
from collections import namedtuple
from copy import deepcopy


input_file = open("Day_23/input", "r")
input_file = open("Day_23/sample_input", "r")
lines = [x for x in input_file.readlines()]


move_costs = {
    'A' : 1,
    'B' : 10,
    'C' : 100,
    'D' : 1000,
}

amphipod_preferred_room = {
    'A' : 1,
    'B' : 2,
    'C' : 3,
    'D' : 4,
}


# positions
#############
#0123456789a# hallway is room 0
###0#0#0#0###
  #1#1#1#1#
  #########
#  1 2 3 4   <- rooms

room_to_hallway = {
    1: 2,
    2: 4,
    3: 6,
    4: 8,
}

Position = namedtuple("Position", "room pos")


class Move(namedtuple("Move", "start end cost")):
    def __repr__(self) -> str:
        return f"{self.start.room}:{self.start.pos}->{self.end.room}:{self.end.pos}|{self.cost}"


all_positions = []
all_positions.extend([Position(0, i) for i in range(11)])
all_positions.extend([Position(i, 0) for i in range(1,5)])
all_positions.extend([Position(i, 1) for i in range(1,5)])
all_positions.extend([Position(i, 2) for i in range(1,5)])
all_positions.extend([Position(i, 3) for i in range(1,5)])

# Cache paths so we're not recreating a bunch of times
path_position_lookup_table = {}

def get_path_positions(start : Position, end : Position) -> list[Position]:
    if (start, end) in path_position_lookup_table:
        return path_position_lookup_table[(start, end)]

    path = []
    # Exit room further, if required
    if start.room > 0 and start.pos > 0:

        path.append(Position(start.room, 0))

    # Get corridor range
    corridor_start = start.pos
    if start.room > 0:
        corridor_start = room_to_hallway[start.room]
    
    corridor_end = end.pos
    if end.room > 0:
        corridor_end = room_to_hallway[end.room]
    
    diff = 1 if corridor_end > corridor_start else -1
    if start.room == 0:
        corridor_start += diff
    if end.room != 0:
        corridor_end += diff
    
    # Get corridor path
    corridor = corridor_start
    while corridor != corridor_end:
        path.append(Position(0, corridor))
        corridor += diff

    # Enter room further, if required
    if end.room > 0 and end.pos > 0:
        path.append(Position(end.room, 0))

    path_position_lookup_table[(start, end)] = path

    return path


success = [
    [None] * 11,
    ['A'] * 2,
    ['B'] * 2,
    ['C'] * 2,
    ['D'] * 2,
]


class Burrow:
    rooms : list[list[str]]
    cost : int

    def __init__(self, rooms : list[list[str]], cost : int = 0):
        self.rooms = rooms
        self.cost = cost
    
    def _get_hallway_as_str(self) -> str:
        return "".join([spot if spot else "." for spot in self.rooms[0]])
    
    def _get_bed(self, room : int, pos : int) -> str:
        if self.rooms[room][pos]:
            return self.rooms[room][pos]
        return "."
    
    def get_valid_moves(self) -> list[Move]:
        moves = []
        for start in all_positions:
            # No point moving an empty spot
            amphipod = self.rooms[start.room][start.pos]
            if not amphipod:
                continue
            # Don't move if we're already in the back of the correct room
            if start.pos == 1 and start.room == amphipod_preferred_room[amphipod]:
                continue
            # Don't move if we're in the front of the correct room, with the correct other occupant
            other_occupant = self.rooms[start.room][1]
            if other_occupant and start.pos == 0 and start.room == amphipod_preferred_room[amphipod] and start.room == amphipod_preferred_room[other_occupant]:
                continue
            for end in all_positions:
                # Can't move to occupied spot
                if self.rooms[end.room][end.pos]:
                    continue
                # Moving to room
                if end.room != 0:
                    # Move should be from hallway to room, or room to hallway
                    if start.room != 0:
                        continue
                    # Won't move to the wrong room
                    if end.room != amphipod_preferred_room[amphipod]:
                        continue
                    # Won't move to a room if the room is occupied with the wrong type
                    back_of_room = self.rooms[end.room][1]
                    if back_of_room and amphipod_preferred_room[back_of_room] != end.room:
                        continue
                    # Don't move to the front of an empty room
                    if end.pos == 0 and not back_of_room:
                        continue
                # Moving to corridor
                else:
                    # Move should be from hallway to room, or room to hallway
                    if start.room == 0:
                        continue 
                    # Won't stop in hallway, outside a room
                    if end.pos in room_to_hallway.values():
                        continue
                # If the path is blocked, we can't move either
                path = get_path_positions(start, end)
                blocked = False
                for step in path:
                    if self.rooms[step.room][step.pos]:
                        blocked = True
                        break
                if blocked:
                    continue

                move = Move(start, end, (len(path) + 1) * move_costs[amphipod])
                moves.append(move)
        return moves
    
    def apply_move(self, move: Move) -> "Burrow":
        # create a copy of the rooms, swap the start and end, add cost and create a new borrow
        new_rooms = deepcopy(self.rooms)
        # Could swap but end should be None anyway
        new_rooms[move.end.room][move.end.pos] = self.rooms[move.start.room][move.start.pos]
        new_rooms[move.start.room][move.start.pos] = None
        return Burrow(new_rooms, self.cost + move.cost)
    
    def is_complete(self) -> bool:
        return self.rooms == success
    
    def __repr__(self) -> str:
        repr_str = "#############\n"
        repr_str += "#" + self._get_hallway_as_str() + "#\n"
        for i in range(len(self.rooms[1])):
           repr_str += "###" + self._get_bed(1,i) + "#" + self._get_bed(2,i) + "#"
           repr_str += self._get_bed(3,i) + "#" + self._get_bed(4,i) + "###\n"
        repr_str += "  #########  \n"
        return repr_str


# Part 1
print("Part 1:")

rooms = [
    [None] * 11,
    [lines[2][3], lines[3][3]],
    [lines[2][5], lines[3][5]],
    [lines[2][7], lines[3][7]],
    [lines[2][9], lines[3][9]],
]

class StackItem:
    burrow : Burrow
    move_list : list[Move]
    move_record : list[Move]

    def __init__(self, burrow : Burrow, path_limit : int, move_record : list[Move] = []):
        self.burrow = burrow
        new_moves = [move for move in burrow.get_valid_moves() if burrow.cost + move.cost < path_limit]
        self.move_list = sorted(new_moves, key=lambda x: x[2], reverse=True)

        self.move_record = move_record
    
    def get_next_move(self, path_limit : int) -> "StackItem":
        move = self.move_list.pop()
        new_burrow = self.burrow.apply_move(move)
        return StackItem(new_burrow, path_limit, self.move_record + [move])


best_cost = 9223372036854775807
stack = [StackItem(Burrow(rooms), best_cost)]
tests = 0
found = 0

# This is super slow and inefficient - does get there eventually, but it's not good

while stack:
    stack_item = stack[-1]
    tests += 1
    # Debug
    # print(f"{stack_item.move_record}")
    if tests % 1000000 == 0:
        print(f"Still working (Best cost: {best_cost}, stack: {len(stack)}, moves: {stack_item.move_record}, tests: {tests})")
    # If we've got a path in budget, mark it
    if stack_item.burrow.is_complete():
        found += 1
        best_cost = min(best_cost, stack_item.burrow.cost)
        print(f"New best cost: {best_cost}, stack: {len(stack)}, moves: {stack_item.move_record}, tests: {tests}")
    # If there are no moves left, drop from list
    elif not stack_item.move_list:
        stack.pop()
    # We potentially have better solutions this way
    else:
        new_stack_item = stack_item.get_next_move(best_cost)
        # Don't add if already more expensive than best cost
        if new_stack_item.burrow.cost <= best_cost:
            stack.append(new_stack_item)
        else:
            # That was the best cost for this stack so just drop the current one
            stack.pop()

    # Move backwards in the stack until the cost is better than the current best
    while stack and stack[-1].burrow.cost >= best_cost:
        stack.pop()

print(f"Best cost: {best_cost}, stack: {len(stack)}, moves: {stack_item.move_record}, tests: {tests}")

print(f"Result: {best_cost}")

# Part 2
print("Part 2:")

# rooms = [
#     [None] * 11,
#     [lines[2][3], 'D', 'D', lines[3][3]],
#     [lines[2][5], 'C', 'B', lines[3][5]],
#     [lines[2][7], 'B', 'A', lines[3][7]],
#     [lines[2][9], 'A', 'C', lines[3][9]],
# ]

# burrow = Burrow(rooms)
# print(f"{burrow}")





part_02 = "not implemented yet"
print(f"Result: {part_02}")
