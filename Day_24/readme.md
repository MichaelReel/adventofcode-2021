This one was a nightmare. Restarted a number of times. Nearly got there with a large expression frame but eventually
had to resort to reddit to pick up some tips. Still took time and I'm not 100% happy with the code here.

I included an "old" approach simply because I wrote a load of code and didn't want to throw it away. It still doesn't work.

```
--- Day 24: Arithmetic Logic Unit ---

Magic smoke starts leaking from the submarine's arithmetic logic unit (ALU). Without the ability to perform basic arithmetic and logic functions, the submarine can't produce cool patterns with its Christmas lights!

It also can't navigate. Or run the oxygen system.

Don't worry, though - you probably have enough oxygen left to give you enough time to build a new ALU.

The ALU is a four-dimensional processing unit: it has integer variables w, x, y, and z. These variables all start with the value 0. The ALU also supports six instructions:

    inp a - Read an input value and write it to variable a.
    add a b - Add the value of a to the value of b, then store the result in variable a.
    mul a b - Multiply the value of a by the value of b, then store the result in variable a.
    div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
    mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
    eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.

In all of these instructions, a and b are placeholders; a will always be the variable where the result of the operation is stored (one of w, x, y, or z), while b can be either a variable or a number. Numbers can be positive or negative, but will always be integers.

The ALU has no jump instructions; in an ALU program, every instruction is run exactly once in order from top to bottom. The program halts after the last instruction has finished executing.

(Program authors should be especially cautious; attempting to execute div with b=0 or attempting to execute mod with a<0 or b<=0 will cause the program to crash and might even damage the ALU. These operations are never intended in any serious ALU program.)

For example, here is an ALU program which takes an input number, negates it, and stores it in x:

inp x
mul x -1

Here is an ALU program which takes two input numbers, then sets z to 1 if the second input number is three times larger than the first input number, or sets z to 0 otherwise:

inp z
inp x
mul z 3
eql z x

Here is an ALU program which takes a non-negative integer as input, converts it into binary, and stores the lowest (1's) bit in z, the second-lowest (2's) bit in y, the third-lowest (4's) bit in x, and the fourth-lowest (8's) bit in w:

inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2

Once you have built a replacement ALU, you can install it in the submarine, which will immediately resume what it was doing when the ALU failed: validating the submarine's model number. To do this, the ALU will run the MOdel Number Automatic Detector program (MONAD, your puzzle input).

Submarine model numbers are always fourteen-digit numbers consisting only of digits 1 through 9. The digit 0 cannot appear in a model number.

When MONAD checks a hypothetical fourteen-digit model number, it uses fourteen separate inp instructions, each expecting a single digit of the model number in order of most to least significant. (So, to check the model number 13579246899999, you would give 1 to the first inp instruction, 3 to the second inp instruction, 5 to the third inp instruction, and so on.) This means that when operating MONAD, each input instruction should only ever be given an integer value of at least 1 and at most 9.

Then, after MONAD has finished running all of its instructions, it will indicate that the model number was valid by leaving a 0 in variable z. However, if the model number was invalid, it will leave some other non-zero value in z.

MONAD imposes additional, mysterious restrictions on model numbers, and legend says the last copy of the MONAD documentation was eaten by a tanuki. You'll need to figure out what MONAD does some other way.

To enable as many submarine features as possible, find the largest valid fourteen-digit model number that contains no 0 digits. What is the largest model number accepted by MONAD?

Your puzzle answer was 79997391969649.
--- Part Two ---

As the submarine starts booting up things like the Retro Encabulator, you realize that maybe you don't need all these submarine features after all.

What is the smallest model number accepted by MONAD?

Your puzzle answer was 16931171414113.
```


Also, some manual working out I didn't want to throw away either, becuase I'm a hoarder.

```
Part 1:
1: (<unknown(0)> + 8)
2: ((<reference(1)> * ((25 * (((<reference(1)> % 26) + 13) != <unknown(1)>)) + 1)) + ((<unknown(1)> + 8) * (((<reference(1)> % 26) + 13) != <unknown(1)>)))
3: ((<reference(2)> * ((25 * (((<reference(2)> % 26) + 13) != <unknown(2)>)) + 1)) + ((<unknown(2)> + 3) * (((<reference(2)> % 26) + 13) != <unknown(2)>)))
4: ((<reference(3)> * ((25 * (((<reference(3)> % 26) + 12) != <unknown(3)>)) + 1)) + ((<unknown(3)> + 10) * (((<reference(3)> % 26) + 12) != <unknown(3)>)))
5: (((<reference(4)> // 26) * ((25 * (((<reference(4)> % 26) + -12) != <unknown(4)>)) + 1)) + ((<unknown(4)> + 8) * (((<reference(4)> % 26) + -12) != <unknown(4)>)))
6: ((<reference(5)> * ((25 * (((<reference(5)> % 26) + 12) != <unknown(5)>)) + 1)) + ((<unknown(5)> + 8) * (((<reference(5)> % 26) + 12) != <unknown(5)>)))
7: (((<reference(6)> // 26) * ((25 * (((<reference(6)> % 26) + -2) != <unknown(6)>)) + 1)) + ((<unknown(6)> + 8) * (((<reference(6)> % 26) + -2) != <unknown(6)>)))
8: (((<reference(7)> // 26) * ((25 * (((<reference(7)> % 26) + -11) != <unknown(7)>)) + 1)) + ((<unknown(7)> + 5) * (((<reference(7)> % 26) + -11) != <unknown(7)>)))
9: ((<reference(8)> * ((25 * (((<reference(8)> % 26) + 13) != <unknown(8)>)) + 1)) + ((<unknown(8)> + 9) * (((<reference(8)> % 26) + 13) != <unknown(8)>)))
10: ((<reference(9)> * ((25 * (((<reference(9)> % 26) + 14) != <unknown(9)>)) + 1)) + ((<unknown(9)> + 3) * (((<reference(9)> % 26) + 14) != <unknown(9)>)))
11: (((<reference(10)> // 26) * ((25 * ((<reference(10)> % 26) != <unknown(10)>)) + 1)) + ((<unknown(10)> + 4) * ((<reference(10)> % 26) != <unknown(10)>)))
12: (((<reference(11)> // 26) * ((25 * (((<reference(11)> % 26) + -12) != <unknown(11)>)) + 1)) + ((<unknown(11)> + 9) * (((<reference(11)> % 26) + -12) != <unknown(11)>)))
13: (((<reference(12)> // 26) * ((25 * (((<reference(12)> % 26) + -13) != <unknown(12)>)) + 1)) + ((<unknown(12)> + 2) * (((<reference(12)> % 26) + -13) != <unknown(12)>)))
Just solve for: (0 == (((<reference(13)> // 26) * ((25 * (((<reference(13)> % 26) + -6) != <unknown(13)>)) + 1)) + ((<unknown(13)> + 7) * (((<reference(13)> % 26) + -6) != <unknown(13)>))))


1: [9..17]

2: ((<reference(1)> * ((25 * (((<reference(1)> % 26) + 13) != <unknown(1)>)) + 1)) + ((<unknown(1)> + 8) * (((<reference(1)> % 26) + 13) != <unknown(1)>)))
2: ((    [9..17]    * ((25 * (((   [9..17]     % 26) + 13) !=   [1..9]    )) + 1)) + ((   [1..9]    + 8) * (((    [9..17]    % 26) + 13) !=   [1..9]    )))
2: ((    [9..17]    * ((25 * (         [22..30]            !=   [1..9]    )) + 1)) + (       [9..17]     * (          [22..30]           !=   [1..9]    )))
2: ((    [9..17]    * ((25 *                        1                      ) + 1)) + (       [9..17]     *                         1                     ))
2: ((    [9..17]    *                              26                            ) +                       [9..17]                                        )
2: (                         [234..(+26)..442]                                     +                       [9..17]                                        )
2: (                [234,260,286,312,338,364,390,416,442]                          +                       [9..17]                                        )

in 0 map : {1:234 .. 9:442}, in 1 map: {1:9 .. 9:17}


3: ((<reference(2)>        * ((25 * (((<reference(2)>        % 26) + 13) != <unknown(2)>)) + 1)) + ((<unknown(2)> + 3) * (((<reference(2)>        % 26) + 13) != <unknown(2)>)))
3: (([234+26..442]+[9..17] * ((25 * ((([234+26..442]+[9..17] % 26) + 13) !=    [1..9]   )) + 1)) + ((   [1..9]    + 3) * ((([234+26..442]+[9..17] % 26) + 13) !=    [1..9]   )))
3: (([234+26..442]+[9..17] * ((25 * ((               [9..17]       + 13) !=    [1..9]   )) + 1)) + ((   [1..9]    + 3) * ((               [9..17]       + 13) !=    [1..9]   )))
3: (([234+26..442]+[9..17] * ((25 * (               [22..30]             !=    [1..9]   )) + 1)) + (    [4..12]        * (               [22..30]             !=    [1..9]   )))
3: (([234+26..442]+[9..17] * ((25 *                        1                             ) + 1)) + (    [4..12]        *                        1                             ))
3: (([234+26..442]+[9..17] *                                 26                                  +                              [4..12]                                        )
3: ((                   [6084+676..11492]+[234+26..442]                                          +                              [4..12]                                        )

in 0 map : {1:6084 .. 9:11492}, in 1 map: {1:234 .. 9:442}, in 2 map: {1:4 .. 9:12}



(Added some additional refactoring operations)

0: 0
1: [in 1: 9..17]
2: ([in 1: 234..442] + [in 2: 9..17])
3: (([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12])
4: ((([in 1: 158184..298792] + [in 2: 6084..11492]) + [in 3: 104..312]) + [in 4: 11..19])
5: (((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9])))
6: (((((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9]))) * ((25 * ((((((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9]))) % 26) + 12) != [in 6: 1..9])) + 1)) + ([in 6: 9..17] * ((((((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9]))) % 26) + 12) != [in 6: 1..9])))
7: ((((((((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9]))) * ((25 * ((((((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9]))) % 26) + 12) != [in 6: 1..9])) + 1)) // 26) + (([in 6: 9..17] * ((((((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9]))) % 26) + 12) != [in 6: 1..9])) // 26)) * ((25 * (((<reference(6)> % 26) + -2) != [in 7: 1..9])) + 1)) + ([in 7: 9..17] * (((<reference(6)> % 26) + -2) != [in 7: 1..9])))
8: (((((((((((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9]))) * ((25 * ((((((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9]))) % 26) + 12) != [in 6: 1..9])) + 1)) // 26) + (([in 6: 9..17] * ((((((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9]))) % 26) + 12) != [in 6: 1..9])) // 26)) * ((25 * (((<reference(6)> % 26) + -2) != [in 7: 1..9])) + 1)) // 26) + (([in 7: 9..17] * (((<reference(6)> % 26) + -2) != [in 7: 1..9])) // 26)) * ((25 * (((<reference(7)> % 26) + -11) != [in 8: 1..9])) + 1)) + ([in 8: 6..14] * (((<reference(7)> % 26) + -11) != [in 8: 1..9])))
9: ((<reference(8)> * ((25 * (((<reference(8)> % 26) + 13) != [in 9: 1..9])) + 1)) + ([in 9: 10..18] * (((<reference(8)> % 26) + 13) != [in 9: 1..9])))
10: ((<reference(9)> * ((25 * (((<reference(9)> % 26) + 14) != [in 10: 1..9])) + 1)) + ([in 10: 4..12] * (((<reference(9)> % 26) + 14) != [in 10: 1..9])))
11: (((((<reference(9)> * ((25 * (((<reference(9)> % 26) + 14) != [in 10: 1..9])) + 1)) // 26) + (([in 10: 4..12] * (((<reference(9)> % 26) + 14) != [in 10: 1..9])) // 26)) * ((25 * ((<reference(10)> % 26) != [in 11: 1..9])) + 1)) + ([in 11: 5..13] * ((<reference(10)> % 26) != [in 11: 1..9])))
12: ((((((((<reference(9)> * ((25 * (((<reference(9)> % 26) + 14) != [in 10: 1..9])) + 1)) // 26) + (([in 10: 4..12] * (((<reference(9)> % 26) + 14) != [in 10: 1..9])) // 26)) * ((25 * ((<reference(10)> % 26) != [in 11: 1..9])) + 1)) // 26) + (([in 11: 5..13] * ((<reference(10)> % 26) != [in 11: 1..9])) // 26)) * ((25 * (((<reference(11)> % 26) + -12) != [in 12: 1..9])) + 1)) + ([in 12: 10..18] * (((<reference(11)> % 26) + -12) != [in 12: 1..9])))
13: (((((((((((<reference(9)> * ((25 * (((<reference(9)> % 26) + 14) != [in 10: 1..9])) + 1)) // 26) + (([in 10: 4..12] * (((<reference(9)> % 26) + 14) != [in 10: 1..9])) // 26)) * ((25 * ((<reference(10)> % 26) != [in 11: 1..9])) + 1)) // 26) + (([in 11: 5..13] * ((<reference(10)> % 26) != [in 11: 1..9])) // 26)) * ((25 * (((<reference(11)> % 26) + -12) != [in 12: 1..9])) + 1)) // 26) + (([in 12: 10..18] * (((<reference(11)> % 26) + -12) != [in 12: 1..9])) // 26)) * ((25 * (((<reference(12)> % 26) + -13) != [in 13: 1..9])) + 1)) + ([in 13: 3..11] * (((<reference(12)> % 26) + -13) != [in 13: 1..9])))
Just solve for: (0 == ((((((((((((((<reference(9)> * ((25 * (((<reference(9)> % 26) + 14) != [in 10: 1..9])) + 1)) // 26) + (([in 10: 4..12] * (((<reference(9)> % 26) + 14) != [in 10: 1..9])) // 26)) * ((25 * ((<reference(10)> % 26) != [in 11: 1..9])) + 1)) // 26) + (([in 11: 5..13] * ((<reference(10)> % 26) != [in 11: 1..9])) // 26)) * ((25 * (((<reference(11)> % 26) + -12) != [in 12: 1..9])) + 1)) // 26) + (([in 12: 10..18] * (((<reference(11)> % 26) + -12) != [in 12: 1..9])) // 26)) * ((25 * (((<reference(12)> % 26) + -13) != [in 13: 1..9])) + 1)) // 26) + (([in 13: 3..11] * (((<reference(12)> % 26) + -13) != [in 13: 1..9])) // 26)) * ((25 * (((<reference(13)> % 26) + -6) != [in 14: 1..9])) + 1)) + ([in 14: 8..16] * (((<reference(13)> % 26) + -6) != [in 14: 1..9]))))




5: ((([in 1: 6084..11492] + [in 2: 234..442]) + [in 3: 4..12]) * ((25 * ([in 4: -1..7] != [in 5: 1..9])) + 1)) + ([in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9])))

25 * ([in 4: -1..7] != [in 5: 1..9])
this means: 25 if [in 4] -2 != [in 5] else 0

[in 5: 9..17] * ([in 4: -1..7] != [in 5: 1..9])
this means: [in 5] if [in 4] -2 != [in 5] else 0



(At this point I went to reddit)
```