#!/usr/bin/env python3
from typing import Optional, Tuple


input_file = open("Day_18/input", "r")
# input_file = open("Day_18/sample_input", "r")
lines = [x.strip() for x in input_file.readlines()]


class SnailNumber:
    left : Optional["SnailNumber"] = None
    right : Optional["SnailNumber"] = None
    value : Optional[int] = None
    nesting : int = 0

    def __init__(self, string_repr, nesting = 0) -> None:
        self.nesting = nesting
        # We might want to create an empty SnailNumber for addition
        if not string_repr:
            return
        # First char should be a bracket, find matching bracket and comma:
        if string_repr[0] != "[":
            # This is probably a value
            self.value = int(string_repr)
            return
        # Split this into values / other snail_numbers:
        bracket_count = 0
        comma_pos = -1
        index = 1
        while bracket_count >= 0 and index < len(string_repr):
            if string_repr[index] == "[":
                bracket_count += 1
            elif string_repr[index] == "]":
                bracket_count -= 1
            elif bracket_count == 0 and string_repr[index] == ",":
                comma_pos = index
            index += 1
        # Instead of value, add the sub SnailNumbers
        self.left = SnailNumber(string_repr[1:comma_pos], nesting+1)
        self.right = SnailNumber(string_repr[comma_pos+1:-1], nesting+1)


    def add_snail_number(self, other: "SnailNumber") -> "SnailNumber":
        new_snail_number = SnailNumber("")
        self._push_down()
        other._push_down()
        new_snail_number.left = self
        new_snail_number.right = other
        return new_snail_number


    def _push_down(self) -> None:
        self.nesting += 1
        if self.left != None:
            self.left._push_down()
        if self.right != None:
            self.right._push_down()


    def _has_deep_nested(self) -> bool:
        if self.value != None:
            return False
        if self.nesting >= 4:
            return True
        return self.left._has_deep_nested() or self.right._has_deep_nested()


    def _has_big_value(self) -> bool:
        if self.value != None:
            return self.value >= 10
        else:
            return self.left._has_big_value() or self.right._has_big_value()


    def reduce(self) -> None:
        while self._has_deep_nested() or self._has_big_value():
            if self._has_deep_nested():
                self._explode_reduce()
            elif self._has_big_value():
                self._split_reduce()


    def _explode_reduce(self) -> Tuple[bool, int, int]:
        # Create an explosion if the conditions are right
        if self.nesting >= 4 and self.left != None and self.right != None:
            self.value = 0
            (left, right) = (self.left.value, self.right.value)
            self.left = None
            self.right = None
            return True, left, right

        # Work down the left path, until something happens, handle explosions
        if self.left != None:
            explode, left, right = self.left._explode_reduce()
            if explode:
                # If there's a right path, send it down, else up
                if self.right != None:
                    self.right._explode_right(right)
                    right = 0
                return True, left, right

        # Work down the right path, until something happens, handle explosions
        if self.right != None:
            explode, left, right = self.right._explode_reduce()
            if explode:
                # If there's a left path, send it down, else up
                if self.left != None:
                    self.left._explode_left(left)
                    left = 0
                return True, left, right

        # Didn't do anything
        return False, 0, 0


    def _explode_left(self, value: int) -> None:
        # Need to find the next value to the left
        if self.value != None:
            self.value += value
        elif self.right != None:
            self.right._explode_left(value)
        elif self.left != None:
            self.left._explode_left(value)


    def _explode_right(self, value: int) -> None:
        # Need to find the next value to the right
        if self.value != None:
            self.value += value
        elif self.left != None:
            self.left._explode_right(value)
        elif self.right != None:
            self.right._explode_right(value)


    def _split_reduce(self) -> bool:
        # Split this value, if the conditions are right
        if self.value != None and self.value >= 10:
            half_value = self.value // 2
            self.left = SnailNumber(str(half_value), self.nesting + 1)
            self.right = SnailNumber(str(half_value + (1 if half_value * 2 < self.value else 0)), self.nesting + 1)
            self.value = None
            return True, 0, 0

        # Work down the left path, until something happens
        if self.left != None:
            split = self.left._split_reduce()
            if split:
                return True

        # Work down the right path, until something happens, handle explosions
        if self.right != None:
            split = self.right._split_reduce()
            if split:
                return True

        # Didn't do anything
        return False


    def __repr__(self) -> str:
        if self.value != None:
            return f"{self.value}"
        return f"[{self.left},{self.right}]"


    def magnitude(self) -> int:
        if self.value != None:
            return self.value
        return self.left.magnitude() * 3 + self.right.magnitude() * 2


snails = [SnailNumber(line) for line in lines]
snail_total = SnailNumber(lines[0])

for snail in snails[1:]:
    snail_total = snail_total.add_snail_number(snail)
    snail_total.reduce()


# Part 1
print("Part 1:")

part_01 = snail_total.magnitude()
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

max_magnitude = 0
for line_a in lines:
    for line_b in lines:
        # Addition involves nesting, so recreate each snail per addition
        snail_a = SnailNumber(line_a)
        snail_b = SnailNumber(line_b)
        added_snail = snail_a.add_snail_number(snail_b)
        added_snail.reduce()
        magnitude = added_snail.magnitude()
        # print(f"Adding {snail_a} and {snail_b} = {added_snail} (Magnitude: {magnitude})")
        max_magnitude = max(max_magnitude, magnitude)


part_02 = max_magnitude
print(f"Result: {part_02}")
