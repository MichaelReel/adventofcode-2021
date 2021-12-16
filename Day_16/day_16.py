#!/usr/bin/env python3
from math import prod


# If we need to read input, uncomment:
input_file = open("Day_16/input", "r")
lines = [x.strip() for x in input_file.readlines()]
# lines = ["D2FE28"]
# lines = ["38006F45291200"]
# lines = ["8A004A801A8002F478"]
# lines = ["620080001611562C8802118E34"]
# lines = ["C0015000016115A2E0802F182340"]
# lines = ["A0016C880162017C3686B18A3D4780"]
# lines = ["C200B40A82"]                 # finds the sum of 1 and 2, resulting in the value 3.
# lines = ["04005AC33890"]               # finds the product of 6 and 9, resulting in the value 54.
# lines = ["880086C3E88112"]             # finds the minimum of 7, 8, and 9, resulting in the value 7.
# lines = ["CE00C43D881120"]             # finds the maximum of 7, 8, and 9, resulting in the value 9.
# lines = ["D8005AC2A8F0"]               # produces 1, because 5 is less than 15.
# lines = ["F600BC2D8F"]                 # produces 0, because 5 is not greater than 15.
# lines = ["9C005AC2F8F0"]               # produces 0, because 5 is not equal to 15.
# lines = ["9C0141080250320F1802104A08"] # produces 1, because 1 + 3 = 2 * 2.


bin_string = ''.join([bin(int(hex_char, 16))[2:].zfill(4) for hex_char in lines[0]])
# print(f"{bin_string}")

# Part 1
print("Part 1:")

def parse_packet_from_binary_string(bin_string : str):
    packet = 0
    version = int(bin_string[packet:packet+3], 2)
    version_total = version
    type = int(bin_string[packet+3:packet+6], 2)
    # print(f"V: {version}, T: {type}")
    if type == 4:
        literal_binstr = ""
        # Literal
        literal_group = packet + 6
        prefix = "1"
        lit_length = 0
        while prefix == "1":
            prefix = bin_string[literal_group]
            literal_binstr += bin_string[literal_group+1:literal_group+5]
            literal_group += 5
        literal_value = int(literal_binstr, 2)
        packet = literal_group
        # print(f"literal: {literal_value}, {packet}")
    else:
        # Operator
        length_bit = bin_string[packet + 6]
        if length_bit == "0":
            total_length = int(bin_string[packet+7:packet+22],2)
            sub_packet = packet + 22
            packet += 22 + total_length
            while sub_packet + 7 < packet:
                version_sum, packet_length = parse_packet_from_binary_string(bin_string[sub_packet:])
                sub_packet += packet_length
                version_total += version_sum
            # print(f"total_length: {total_length}, {packet}")
        else:
            number_of_packets = int(bin_string[packet+7:packet+18],2)
            # print(f"number_of_packets: {number_of_packets}")
            sub_packet = packet + 18
            for num in range(number_of_packets):
                version_sum, packet_length = parse_packet_from_binary_string(bin_string[sub_packet:])
                version_total += version_sum
                sub_packet += packet_length
            packet = sub_packet
    return (version_total, packet)

sub_packet = 0
while sub_packet + 7 < len(bin_string):
    version_total, packet_length = parse_packet_from_binary_string(bin_string[sub_packet:])
    sub_packet += packet_length
    # print(f"{version_total}, {packet_length}")

part_01 = version_total
print(f"Result: {part_01}")

# Part 2
print("Part 2:")

def eval_packet(bin_string : str):
    packet = 0
    type = int(bin_string[packet+3:packet+6], 2)
    # print(f"V: {version}, T: {type}")
    if type == 4:
        literal_binstr = ""
        # Literal
        literal_group = packet + 6
        prefix = "1"
        lit_length = 0
        while prefix == "1":
            prefix = bin_string[literal_group]
            literal_binstr += bin_string[literal_group+1:literal_group+5]
            literal_group += 5
        literal_value = int(literal_binstr, 2)
        packet = literal_group
        return (literal_value, packet)
    else:
        literal_value = 0
        sub_literals = []
        # Operator
        length_bit = bin_string[packet + 6]
        if length_bit == "0":
            total_length = int(bin_string[packet+7:packet+22],2)
            sub_packet = packet + 22
            packet += 22 + total_length
            while sub_packet + 7 < packet:
                sub_literal, packet_length = eval_packet(bin_string[sub_packet:])
                sub_packet += packet_length
                sub_literals.append(sub_literal)
        else:
            number_of_packets = int(bin_string[packet+7:packet+18],2)
            sub_packet = packet + 18
            for num in range(number_of_packets):
                sub_literal, packet_length = eval_packet(bin_string[sub_packet:])
                sub_packet += packet_length
                sub_literals.append(sub_literal)
            packet = sub_packet
        if type == 0:
            return (sum(sub_literals), packet)
        elif type == 1:
            return (prod(sub_literals), packet)
        elif type == 2:
            return (min(sub_literals), packet)
        elif type == 3:
            return (max(sub_literals), packet)
        elif type == 5:
            return (1 if sub_literals[0] > sub_literals[1] else 0,packet)
        elif type == 6:
            return (1 if sub_literals[0] < sub_literals[1] else 0,packet)
        elif type == 7:
            return (1 if sub_literals[0] == sub_literals[1] else 0,packet)
        
        return (literal_value, packet)

sub_packet = 0
while sub_packet + 7 < len(bin_string):
    evaluation, packet_length = eval_packet(bin_string[sub_packet:])
    sub_packet += packet_length

part_02 = evaluation
print(f"Result: {part_02}")
