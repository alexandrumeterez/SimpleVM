"""
    Declare the bytecodes for the VM
"""

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

OPCODES = [
    '',
    'IADD',
    'ISUB',
    'IMUL',
    'ILT',
    'IEQ',
    'BR',
    'BRT',
    'BRF',
    'ICONST',
    'LOAD',
    'GLOAD',
    'STORE',
    'GSTORE',
    'PRINT',
    'POP',
    'HALT'
]
