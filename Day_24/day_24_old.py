#!/usr/bin/env python3
from collections import namedtuple
from typing import Optional


input_file = open("Day_24/input", "r")
lines = [x.strip() for x in input_file.readlines()]

Instruction = namedtuple("Instruction", "operator variable value")

# Silly "Round to zero" division - not really standard:
def sign(value : int) -> int:
    return 1 if value > 0 else -1 if value < 0 else 0

def div(a : int, b : int) -> int:
    return abs(a) // abs(b) * sign(a) * sign(b)


class Expression():
    def refactor(self) -> "Expression":
        return self

    def has_reference(self, index):
        return False
    
    def pull_up_references(self) -> "Expression":
        return self
    
    def get_all_unknowns(self) -> list["Expression"]:
        return []


class ExpressionReference(Expression):
    index : int = 0
    references : list[Expression] = []

    def __init__(self, expression: Expression) -> None:
        ExpressionReference.references.append(expression)
        self.index = ExpressionReference.index
        ExpressionReference.index += 1

    def __repr__(self) -> str:
        return f"<reference({self.index})>"
    
    def refactor(self) -> Expression:
        ExpressionReference.references[self.index].refactor()
        return self
    
    def has_reference(self, index):
        return self.index == index
    
    def pull_up_references(self) -> Expression:
        return ExpressionReference.references[self.index].refactor()
    
    def get_all_unknowns(self) -> list[Expression]:
        return ExpressionReference.references[self.index].get_all_unknowns()


class UnknownVariable(Expression):
    index : int = 0
    def __init__(self, index : Optional[int] = None, value_map : Optional[dict] = {i:i for i in range(1,10)}) -> None:
        if index:
            self.index = index
        else:
            self.index = UnknownVariable.index
            UnknownVariable.index += 1
        self.value_map = value_map

    def __repr__(self) -> str:
        return f"[in {self.index}: {self.value_map[1]}..{self.value_map[9]}]"
    
    def mapped(self, inst, value) -> "UnknownVariable":
        mapped_unknown = UnknownVariable(self.index, self.value_map.copy())
        if inst == "+":
            for key in mapped_unknown.value_map:
                mapped_unknown.value_map[key] += value
        if inst == "*":
            for key in mapped_unknown.value_map:
                mapped_unknown.value_map[key] *= value
        if inst == "//":
            for key in mapped_unknown.value_map:
                mapped_unknown.value_map[key] = div(mapped_unknown.value_map[key], value)
        if inst == "%":
            for key in mapped_unknown.value_map:
                mapped_unknown.value_map[key] %= value
        # If all the values end up the same, return a literal instead
        values = list(mapped_unknown.value_map.values())
        if values.count(values[0]) == len(values):
            return Literal(values[0])

        return mapped_unknown
    
    def get_all_unknowns(self) -> list[Expression]:
        return [self]


class Literal(Expression):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self) -> str:
        return f"{self.value}"


class RangeVariable(Expression):
    def __init__(self, start : Expression, end : Expression):
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"[{self.start}..{self.end}]"


class Calculation(Expression):
    def __init__(self, a : Expression, b : Expression, type : str):
        self.a = a
        self.b = b
        self.type = type
    
    def __repr__(self) -> str:
        return f"({self.a} {self.type} {self.b})"

    def has_reference(self, index):
        return self.a.has_reference(index) or self.b.has_reference(index)
    
    def pull_up_references(self) -> Expression:
        self.a = self.a.pull_up_references()
        self.b = self.b.pull_up_references()
        return self
    
    def get_all_unknowns(self) -> list[Expression]:
        return self.a.get_all_unknowns() + self.b.get_all_unknowns()


class Division(Calculation):
    def __init__(self, a : Expression, b : Expression) -> None:
        super().__init__(a, b, "//")

    def refactor(self) -> Expression:
        a = self.a if not isinstance(self.a, ExpressionReference) else ExpressionReference.references[self.a.index]
        b = self.b if not isinstance(self.b, ExpressionReference) else ExpressionReference.references[self.b.index]
        if isinstance(a, Literal):
            if isinstance(b, Literal):
                return Literal(div(a.value, b.value))
            if a.value == 0:
                return Literal(0)
        if isinstance(b, Literal):
            if b.value == 1:
                return self.a.refactor()
            if isinstance(a, UnknownVariable):
                return a.mapped("//", b.value)
            if isinstance(a, Addition):
                return a.div_operators(b)
        return super().refactor()


class Addition(Calculation):
    def __init__(self, a : Expression, b : Expression) -> None:
        super().__init__(a, b, "+")

    def refactor(self) -> Expression:
        a = self.a if not isinstance(self.a, ExpressionReference) else ExpressionReference.references[self.a.index]
        b = self.b if not isinstance(self.b, ExpressionReference) else ExpressionReference.references[self.b.index]
        if isinstance(a, Literal):
            if isinstance(b, Literal):
                return Literal(a.value + b.value)
            if a.value == 0:
                return self.b.refactor()
            if isinstance(b, UnknownVariable):
                return b.mapped("+", a.value)
        if isinstance(b, Literal):
            if b.value == 0:
                return self.a.refactor()
            if isinstance(a, UnknownVariable):
                return a.mapped("+", b.value)
        return super().refactor()
    
    def mod_operators(self, value) -> Expression:
        # If we mod an internal range in this addition and it returns a literal(0)
        # we can just replace this expression with the other side of the expression
        a = self.a if not isinstance(self.a, ExpressionReference) else ExpressionReference.references[self.a.index]
        b = self.b if not isinstance(self.b, ExpressionReference) else ExpressionReference.references[self.b.index]
        if isinstance(a, UnknownVariable):
            mapped = a.mapped("%", value)
            if isinstance(mapped, Literal) and mapped.value == 0:
                return self.b
        if isinstance(a, Addition):
            new_a = a.mod_operators(value)
            if new_a != a:
                return Addition(new_a, self.b).refactor()
        return self
    
    def mul_operators(self, multiplier: Expression) -> "Addition":
        return Addition(
            Multiplication(self.a, multiplier).refactor(),
            Multiplication(self.b, multiplier).refactor(),
        ).refactor()
    
    def div_operators(self, divisor: Expression) -> "Addition":
        return Addition(
            Division(self.a, divisor).refactor(),
            Division(self.b, divisor).refactor(),
        ).refactor()


class Multiplication(Calculation):
    def __init__(self, a : Expression, b : Expression) -> None:
        super().__init__(a, b, "*")
    
    def refactor(self) -> Expression:
        a = self.a if not isinstance(self.a, ExpressionReference) else ExpressionReference.references[self.a.index]
        b = self.b if not isinstance(self.b, ExpressionReference) else ExpressionReference.references[self.b.index]
        if isinstance(a, Literal):
            if isinstance(b, Literal):
                return Literal(a.value * b.value)
            if a.value == 0:
                return Literal(0)
            if a.value == 1:
                return self.b.refactor()
            if isinstance(b, UnknownVariable):
                return b.mapped("*", a.value)
            if isinstance(b, Addition):
                # If we multiply a literal by addition, we can multiply both sides of the addition
                return b.mul_operators(a)
        if isinstance(b, Literal):
            if b.value == 0:
                return Literal(0)
            if b.value == 1:
                return self.a.refactor()
            if isinstance(a, UnknownVariable):
                return a.mapped("*", b.value)
            if isinstance(a, Addition):
                # If we multiply a literal by addition, we can multiply both sides of the addition
                return a.mul_operators(b)
        return super().refactor()


class Modulus(Calculation):
    def __init__(self, a : Expression, b : Expression) -> None:
        super().__init__(a, b, "%")
    
    def refactor(self) -> "Expression":
        a = self.a if not isinstance(self.a, ExpressionReference) else ExpressionReference.references[self.a.index]
        b = self.b if not isinstance(self.b, ExpressionReference) else ExpressionReference.references[self.b.index]
        if isinstance(a, Literal):
            if isinstance(b, Literal):
                return Literal(a.value % b.value)
            if a.value == 0:
                return Literal(0)
            if isinstance(b, UnknownVariable):
                return b.mapped("%", a.value)
        if isinstance(b, Literal):
            if  b.value == 1:
                return Literal(0)
            if isinstance(a, UnknownVariable):
                return a.mapped("%", b.value)
            # Getting very specific now, if a is an Addition of ranges, mod both ranges
            if isinstance(a, Addition):
                new_a = a.mod_operators(b.value)
                if new_a != a:
                    return Modulus(new_a, self.b).refactor()
        return super().refactor()


class Inequality(Calculation):
    def __init__(self, a : Expression, b : Expression) -> None:
        super().__init__(a, b, "!=")
    
    def refactor(self) -> Expression:
        a = self.a if not isinstance(self.a, ExpressionReference) else ExpressionReference.references[self.a.index]
        b = self.b if not isinstance(self.b, ExpressionReference) else ExpressionReference.references[self.b.index]
        # Evaluate if literals available
        if isinstance(a, Literal) and isinstance(b, Literal):
            return Literal(0 if a.value == b.value else 1)
        # Inputs (Unknowns) can't equal less than 1 or greater than 9
        if isinstance(a, UnknownVariable) and isinstance(b, Literal):
            if b.value < 1 or b.value > 9:
                return Literal(1)
        if isinstance(a, Literal) and isinstance(b, UnknownVariable):
            if a.value < 1 or a.value > 9:
                return Literal(1)
        # If we have ranges that don't overlap, this can be a literal true
        if isinstance(a, UnknownVariable):
            if isinstance(b, UnknownVariable):
                if a.value_map[1] > b.value_map[9] or a.value_map[9] < b.value_map[1]:
                    return Literal(1)
            if isinstance(b, Literal):
                if a.value_map[1] > b.value or a.value_map[9] < b.value:
                    return Literal(1)
        # Where (in)equalities equal 1 or 0, we can trim down
        if isinstance(a, Inequality) and isinstance(b, Literal):
            if b.value == 0:
                return self.a.refactor()
            if b.value == 1:
                return Equality(a.a, a.b).refactor()
        if isinstance(a, Literal) and isinstance(b, Inequality):
            if a.value == 0:
                return self.b.refactor()
            if a.value == 1:
                return Equality(b.a, b.b).refactor()
        if isinstance(a, Equality) and isinstance(b, Literal):
            if b.value == 0:
                return self.a.refactor()
            if b.value == 1:
                return Inequality(a.a, a.b).refactor()
        if isinstance(a, Literal) and isinstance(b, Equality):
            if a.value == 0:
                return self.b.refactor() 
            if a.value == 1:
                return Inequality(b.a, b.b).refactor()
        return super().refactor()


class Equality(Calculation):
    def __init__(self, a : Expression, b : Expression) -> None:
        super().__init__(a, b, "==")
    
    def refactor(self) -> Expression:
        a = self.a if not isinstance(self.a, ExpressionReference) else ExpressionReference.references[self.a.index]
        b = self.b if not isinstance(self.b, ExpressionReference) else ExpressionReference.references[self.b.index]
        if isinstance(a, Literal) and isinstance(b, Literal):
            return Literal(1 if a.value == b.value else 0)
        # Inputs (Unknowns) can't equal less than 1 or greater than 9
        if isinstance(a, UnknownVariable) and isinstance(b, Literal):
            if b.value < 1 or b.value > 9:
                return Literal(0)
        if isinstance(a, Literal) and isinstance(b, UnknownVariable):
            if a.value < 1 or a.value > 9:
                return Literal(0)
        # If we have ranges that don't overlap, this can be a literal false
        if isinstance(a, UnknownVariable):
            if isinstance(b, UnknownVariable):
                if a.value_map[1] > b.value_map[9] or a.value_map[9] < b.value_map[1]:
                    return Literal(0)
            if isinstance(b, Literal):
                if a.value_map[1] > b.value or a.value_map[9] < b.value:
                    return Literal(0)
        # Where (in)equalities equal 1 or 0, we can trim down
        if isinstance(a, Equality) and isinstance(b, Literal):
            if b.value == 0:
                return Inequality(a.a, a.b).refactor()
            if b.value == 1:
                return self.a.refactor()
        if isinstance(a, Literal) and isinstance(b, Equality):
            if a.value == 0:
                return Inequality(b.a, b.b).refactor()
            if a.value == 1:
                return self.b.refactor()
        if isinstance(a, Inequality) and isinstance(b, Literal):
            if b.value == 0:
                return Equality(a.a, a.b).refactor()
            if b.value == 1:
                return self.a.refactor()
        if isinstance(a, Literal) and isinstance(b, Inequality):
            if a.value == 0:
                return Equality(b.a, b.b).refactor()
            if a.value == 1:
                return self.b.refactor()
        return super().refactor()


class ALU:
    def __init__(self, program : list[Instruction]) -> None:
        self.mem = {
            'w' : Literal(0),
            'x' : Literal(0),
            'y' : Literal(0),
            'z' : Literal(0),
        }
        self.program = program
    
    def build_program_expression(self) -> dict[str, int]:
        for ins in self.program:
            if ins.operator == "inp":
                self._inp(ins.variable)
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
        return self.mem

    def _inp(self, store) -> None:
        # Stash off the current 'z' mems
        self.mem['z'] = ExpressionReference(self.mem['z'])
        self.mem[store] = UnknownVariable()

    def _add(self, store, value_str) -> None:
        value = self._get_value(value_str)
        self.mem[store] = Addition(self.mem[store], value).refactor()

    def _mul(self, store, value_str) -> None:
        value = self._get_value(value_str)
        self.mem[store] = Multiplication(self.mem[store], value).refactor()

    def _div(self, store, value_str) -> None:
        value = self._get_value(value_str)
        self.mem[store] = Division(self.mem[store], value).refactor()

    def _mod(self, store, value_str) -> None:
        value = self._get_value(value_str)
        self.mem[store] = Modulus(self.mem[store], value).refactor()

    def _eql(self, store, value_str) -> None:
        value = self._get_value(value_str)
        self.mem[store] = Equality(self.mem[store], value).refactor()

    def _get_value(self, value_str) -> Expression:
        if value_str in self.mem:
            return self.mem[value_str]
        return Literal(int(value_str))



# Part 1
print("Part 1:")

instructions = []
for line in lines:
    tokens = line.split(' ')
    value = (tokens[2:3] or (None,))[0]
    instructions.append(Instruction(tokens[0],tokens[1],value))

inst_blocks = []
while instructions:
    if instructions[0].operator == "inp":
        inst_blocks.append([])
    inst_blocks[-1].append(instructions.pop(0))

# print(f"{instructions}")

alu = ALU(inst_blocks[0])
expression = Equality(Literal(0), alu.build_program_expression()['z']).refactor()

for i, er in enumerate(ExpressionReference.references):
    print(f"{i}: {er}")
print(f"Just solve for: {expression}")





# As fun as this is, need a new approach



part_01 = "not implemented yet"
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

part_02 = "not implemented yet"
print(f"Result: {part_02}")
