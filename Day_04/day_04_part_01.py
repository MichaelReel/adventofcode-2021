#!/usr/bin/env python3

from re import T
from typing import List, Optional


input_file = open("Day_04/input", "r")
input_file = open("Day_04/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]

drawn_numbers = [int(dn) for dn in lines[0].split(",")]



class BingoNumber:
    value: int
    marked: bool

    def __init__(self, value : int, marked : bool = False) -> None:
        self.value = value
        self.marked = marked
    
    def __repr__(self) -> str:
        mark_indicate = "*" if self.marked else "-"
        return f"{self.value: >2}{mark_indicate} "
    
    def mark(self) -> None:
        self.marked = True


class BingoCard:
    rows : List[List[BingoNumber]]
    cols : List[List[BingoNumber]]

    def __init__(self, input_lines : List[str]) -> None:
        self.rows = []
        for line in input_lines:
            # Assuming value every 3 characters from index 0
            self.rows.append([BingoNumber(int(col)) for col in line.split(" ") if col])
        
        self.cols = list(list(col) for col in zip(*self.rows))

    def __repr__(self) -> str:
        return_string = "\n"
        for row in self.rows:
            return_string += f"{row}" + "\n"
        return return_string + ""
    
    def draw_number(self, drawn_value : int) -> bool:
        """
        If the number is in here, draw it check for filled rows or cols
        Return true if this card wins
        """
        number_marked = False
        for row in self.rows:
            for col in row:
                if col.value == drawn_value:
                    col.mark()
                    number_marked = True
                    break
            if number_marked:
                break
        
        if self._check_rows():
            return True
        if self._check_cols():
            return True
        return False
    
    def _check_rows(self) -> bool:
        for row in self.rows:
            if len([col for col in row if col.marked]) == len(row):
                # All in rows are marked
                return True
        return False
    
    def _check_cols(self) -> bool:
        for col in self.cols:
            if len([row for row in col if row.marked]) == len(col):
                # All in cols are marked
                return True
        return False
    
    def count_unmarked(self) -> int:
        unmarked_total = 0
        for row in self.rows:
            unmarked_total += sum([col.value for col in row if not col.marked])
        return unmarked_total
        

# Assuming a bingo card every 6 lines from the third line
bingo_cards = []
for card_start in range(2, len(lines), 6):
    bingo_cards.append(BingoCard(lines[card_start:card_start + 5:1]))


# Part 1
print("Part 1:")

winner : Optional[BingoCard] = None
drawn_index = 0
while not winner and drawn_index < len(drawn_numbers):
    drawn_value = drawn_numbers[drawn_index]
    # print(f"DRAWING: {drawn_value}")
    for card in bingo_cards:
        if card.draw_number(drawn_value):
            winner = card
            break
    if winner:
        break
    drawn_index += 1

# print(f"{drawn_numbers}")
# print(f"{bingo_cards}")
# print(f"Winning Card: {winner}")
# print(f"Winnng card unmarked total: {winner.count_unmarked()}")
# print(f"Last Drawn Number: {drawn_numbers[drawn_index]}")

part_01 = drawn_numbers[drawn_index] * winner.count_unmarked()
print(f"Result: {part_01}")
