#!/usr/bin/env python3
from collections import namedtuple
from copy import deepcopy


input_file = open("Day_23/input", "r")
# input_file = open("Day_23/sample_input", "r")
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


def create_path_lookup_table(room_depth : int) -> dict[Position, dict[Position, list[Position]]]:
    # Create cache of paths so we're not re-creating paths a bunch of times

    hall_positions = [Position(0, i) for i in range(11)]
    room_positions = []

    for dep in range(room_depth):
        room_positions.extend([Position(i, dep) for i in range(1,5)])
    all_positions = hall_positions + room_positions

    path_lookup_table = {}
    for a in all_positions:
        #skip paths that end or exit at the entrance to a room
        if a.room == 0 and a.pos in room_to_hallway.values():
            continue
        path_lookup_table[a] = {}

    for a in hall_positions:
        #skip paths that end or exit at the entrance to a room
        if a.pos in room_to_hallway.values():
            continue

        for b in room_positions:
            path = []

            # Exit or Enter room further, if required
            for pos in range(b.pos):
                path.append(Position(b.room, pos))

            corridor_start = min(a.pos + 1, room_to_hallway[b.room])
            corridor_end = max(a.pos - 1, room_to_hallway[b.room])
            for corridor in range(corridor_start, corridor_end + 1):
                path.append(Position(0, corridor))

            path_lookup_table[a][b] = path
            path_lookup_table[b][a] = path
        
    return path_lookup_table


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
        room_depth = len(self.rooms[1])
        moves = []
        for start in path_lookup_table:

            # No point moving an empty spot
            amphipod = self.rooms[start.room][start.pos]
            if not amphipod:
                continue

            # Don't move if we're at the front of a 'correct' room
            if start.room == amphipod_preferred_room[amphipod]:
                if room_depth - start.pos == self.rooms[start.room][start.pos:].count(amphipod):
                    continue
            
            # Maybe don't move if we're not the first non-empty cell in the room
            if start.room > 0:
                if start.pos != self.rooms[start.room][:start.pos].count(None):
                    continue

            for end in path_lookup_table[start]:
                # Can't move to occupied spot
                if self.rooms[end.room][end.pos]:
                    continue
                # Moving to room
                if end.room != 0:
                    # Won't move to the wrong room
                    if end.room != amphipod_preferred_room[amphipod]:
                        continue

                    # Won't move to a room if the room is occupied with the wrong type
                    if room_depth - end.pos - 1 != self.rooms[end.room][end.pos + 1:].count(amphipod):
                        continue

                # Moving to corridor, don't stop in hallway outside a room
                elif end.pos in room_to_hallway.values():
                    continue

                # If the path is blocked, we can't move either
                path = path_lookup_table[start][end]
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
    
    def is_complete(self, success : list[list[str]]) -> bool:
        return self.rooms == success
    
    def __repr__(self) -> str:
        repr_str = "#############\n"
        repr_str += "#" + self._get_hallway_as_str() + "#\n"
        for i in range(len(self.rooms[1])):
           repr_str += "###" + self._get_bed(1,i) + "#" + self._get_bed(2,i) + "#"
           repr_str += self._get_bed(3,i) + "#" + self._get_bed(4,i) + "###\n"
        repr_str += "  #########  \n"
        return repr_str




# # Part 1
# print("Part 1:")

rooms = [
    [None] * 11,
    [lines[2][3], lines[3][3]],
    [lines[2][5], lines[3][5]],
    [lines[2][7], lines[3][7]],
    [lines[2][9], lines[3][9]],
]

success = [
    [None] * 11,
    ['A'] * 2,
    ['B'] * 2,
    ['C'] * 2,
    ['D'] * 2,
]

path_lookup_table = create_path_lookup_table(2)


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


# best_cost = 9223372036854775807
# stack = [StackItem(Burrow(rooms), best_cost)]
# tests = 0
# found = 0

# # This is super slow and inefficient - does get there eventually, but it's not good

# while stack:
#     stack_item = stack[-1]
#     tests += 1
#     # Debug
#     # print(f"{stack_item.move_record}")
#     if tests % 1000000 == 0:
#         print(f"Still working (Best cost: {best_cost}, stack: {len(stack)}, moves: {stack_item.move_record}, tests: {tests})")
#     # If we've got a path in budget, mark it
#     if stack_item.burrow.is_complete():
#         found += 1
#         best_cost = min(best_cost, stack_item.burrow.cost)
#         print(f"New best cost: {best_cost}, stack: {len(stack)}, moves: {stack_item.move_record}, tests: {tests}")
#     # If there are no moves left, drop from list
#     elif not stack_item.move_list:
#         stack.pop()
#     # We potentially have better solutions this way
#     else:
#         new_stack_item = stack_item.get_next_move(best_cost)
#         # Don't add if already more expensive than best cost
#         if new_stack_item.burrow.cost <= best_cost:
#             stack.append(new_stack_item)
#         else:
#             # That was the best cost for this stack so just drop the current one
#             stack.pop()

#     # Move backwards in the stack until the cost is better than the current best
#     while stack and stack[-1].burrow.cost >= best_cost:
#         stack.pop()

# print(f"Best cost: {best_cost}, stack: {len(stack)}, moves: {stack_item.move_record}, tests: {tests}")

# print(f"Result: {best_cost}")

# Part 2
print("Part 2:")

success = [
    [None] * 11,
    ['A'] * 4,
    ['B'] * 4,
    ['C'] * 4,
    ['D'] * 4,
]

rooms = [
    [None] * 11,
    [lines[2][3], 'D', 'D', lines[3][3]],
    [lines[2][5], 'C', 'B', lines[3][5]],
    [lines[2][7], 'B', 'A', lines[3][7]],
    [lines[2][9], 'A', 'C', lines[3][9]],
]

path_lookup_table = create_path_lookup_table(4)

# This does work (it's more or less the same as the stack approach above)
# But the run-time is horrific - Better approach is athogether needed

def find_successful_moves(burrow : Burrow, best_cost : int, move_record : list = []) -> int:
    # Get moves in order of cheapest first
    moves = sorted(burrow.get_valid_moves(), key=lambda x: x[2])
    if not moves:
        if burrow.is_complete(success):
            best_cost = min(best_cost, burrow.cost)
            print(f"New best cost: {best_cost} {move_record}")
        else:
            # print(f"No valid moves to do: {move_record}")
            # print(f"{burrow}")
            pass
    for move in moves:
        if move.cost + burrow.cost < best_cost:
            new_burrow = burrow.apply_move(move)
            if burrow.is_complete(success):
                best_cost = min(best_cost, new_burrow.cost)
                print(f"New best cost: {best_cost} {move_record} + {move}")
                break
            else:
                # print("Step in")
                best_cost = find_successful_moves(new_burrow, best_cost, move_record + [move])
        else:
            # If this move is too costly, don't bother at the rest
            # print("Moves are too costly, roll back")
            break
    return best_cost

start_burrow = Burrow(rooms)
best_cost = find_successful_moves(start_burrow, 9223372036854775807)


print(f"Result: {best_cost}")
