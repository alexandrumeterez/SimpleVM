"""
    Declare the bytecodes for the VM
"""
from vm.instruction import Instruction

IADD = 1
ISUB = 2
IMUL = 3
ILT = 4
IEQ = 5
BR = 6
BRT = 7
BRF = 8
ICONST = 9
LOAD = 10
GLOAD = 11
STORE = 12
GSTORE = 13
PRINT = 14
POP = 15
HALT = 16

INSTRUCTIONS = [
    '',
    Instruction('IADD', 0),  #
    Instruction('ISUB', 0),  #
    Instruction('IMUL', 0),  #
    Instruction('ILT', 0),  #
    Instruction('IEQ', 0),  #
    Instruction('BR', 1), #
    Instruction('BRT', 1), #
    Instruction('BRF', 1), #
    Instruction('ICONST', 1),  #
    Instruction('LOAD', 1),
    Instruction('GLOAD', 1),  #
    Instruction('STORE', 1),
    Instruction('GSTORE', 1),  #
    Instruction('PRINT', 0),  #
    Instruction('POP', 1),
    Instruction('HALT', 0)  #
]
