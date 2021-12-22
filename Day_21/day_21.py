#!/usr/bin/env python3
from collections import namedtuple
from re import match


# If we need to read input, uncomment:
input_file = open("Day_21/input", "r")
lines = [x.strip() for x in input_file.readlines()]
# lines = [
#     "Player 1 starting position: 4",
#     "Player 2 starting position: 8",
# ]


class Player:
    name : str
    position : int
    score : int

    def __init__(self, name : str, start : int, score : int = 0) -> None:
        self.name = name
        self.position = start
        self.score = score

    def move(self, score: int) -> None:
        zero_index_pos = (self.position - 1 + score) % 10
        self.position = zero_index_pos + 1
        self.score += self.position


class DeterministicDie:
    side : int
    rolls : int

    def __init__(self) -> None:
        self.side = 1
        self.rolls = 0
    
    def roll(self) -> int:
        rolled_side = self.side
        self.rolls += 1
        self.side += 1
        if self.side > 100:
            self.side -= 100

        return rolled_side


players = []
for line in lines:
    player_dict = match(r"^(?P<name>Player \d+) starting position: (?P<start>\d)+$", line).groupdict()
    players.append(Player(player_dict["name"], int(player_dict["start"])))

# Part 1
print("Part 1:")

die = DeterministicDie()

scores = [p.score for p in players]
while max(scores) < 1000:
    for player in players:
        rolls = [die.roll() for _ in range(3)]
        player.move(sum(rolls))
        # print(f"{player.name} rolls {rolls} and moves to space {player.position} for a total score of {player.score}")
        if player.score >= 1000:
            break
    scores = [p.score for p in players]

print(f"losing_score: {min(scores)}, total_rolls: {die.rolls}")

part_01 = min(scores) * die.rolls
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

scores_to_spinoffs = {
    9 : 1,  # 3, 3, 3
    8 : 3,  # 2, 3, 3 | 3, 2, 3 | 3, 3, 2
    7 : 6,  # 1, 3, 3 | 3, 1, 3 | 3, 3, 1 | 2, 2, 3 | 2, 3, 2 | 3, 2, 2
    6 : 7,  # 1, 2, 3 | 1, 3, 2 | 2, 1, 3 | 2, 3, 1 | 3, 1, 2 | 3, 2, 1 | 2, 2, 2
    5 : 6,  # 1, 2, 2 | 2, 1, 2 | 2, 2, 1 | 1, 1, 3 | 1, 3, 1 | 3, 1, 1
    4 : 3,  # 1, 1, 2 | 1, 2, 1 | 2, 1, 1
    3 : 1,  # 1, 1, 1
}

players = []
for line in lines:
    player_dict = match(r"^(?P<name>Player \d+) starting position: (?P<start>\d)+$", line).groupdict()
    players.append(Player(player_dict["name"], int(player_dict["start"])))

class Universe(namedtuple("Universe", "player1 player2 duplicates")):
    pass


universes = [
    Universe(players[0], players[1], 1)
]

player_1_wins = 0
player_2_wins = 0
turn = 0
total_turns = 0

while universes:
# for _ in range(3):

    new_universes = []
    for universe in universes:
        orig_player_1 = universe.player1
        orig_player_2 = universe.player2
        if turn == 0:
        
            # Create a new set of universes for player 1 move
            for score, duplicates in scores_to_spinoffs.items():
                new_player_1 = Player(orig_player_1.name, orig_player_1.position, orig_player_1.score)
                new_player_2 = Player(orig_player_2.name, orig_player_2.position, orig_player_2.score)

                new_player_1.move(score)
                # if player 1 wins don't keep, just get scores, otherwise keep universe
                if new_player_1.score >= 21:
                    player_1_wins += universe.duplicates * duplicates
                else:
                    new_universe = Universe(new_player_1, new_player_2, universe.duplicates * duplicates)
                    new_universes.append(new_universe)


        else:

            # Create a new set of universes for player 2 move
            for score, duplicates in scores_to_spinoffs.items():
                new_player_1 = Player(orig_player_1.name, orig_player_1.position, orig_player_1.score)
                new_player_2 = Player(orig_player_2.name, orig_player_2.position, orig_player_2.score)

                new_player_2.move(score)
                # if player_2 wins don't keep, just get scores, otherwise keep universe
                if new_player_2.score >= 21:
                    player_2_wins += universe.duplicates * duplicates
                else:
                    new_universe = Universe(new_player_1, new_player_2, universe.duplicates * duplicates)
                    new_universes.append(new_universe)

    universes = new_universes
    total_turns += 1
    turn = (turn + 1) % 2

    # Keep this or it looks like it's not doing anything:
    print(f"tt: {total_turns}, p1: {player_1_wins}, p2: {player_2_wins}, unis: {len(universes)}")

part_02 = max(player_1_wins, player_2_wins)
print(f"Result: {part_02}")
