import sys

sys.path.append('..')

from vm.bytecode import *
from vm.virtualmachine import VM

# fibonacci
def run():
    hello = [
        # check if less than 3 as base case
        LOAD, -3, #0
        ICONST, 3, #2
        ILT, #4
        BRF, 10, #5
        ICONST, 1, #7
        RET, #9

        LOAD, -3, #10
        ICONST, 1, #12
        ISUB, #14
        CALL, 0, 1,#15
        LOAD, -3,#18
        ICONST, 2, #20
        ISUB,#22
        CALL, 0, 1,#23
        IADD,#26
        RET,#27

        ICONST, 1,#28
        ICONST, 1,#30
        ICONST, 7,#32
        CALL, 0, 1,#34
        PRINT,
        HALT
    ]
    vm = VM(hello, 28, 100, 100)
    vm.cpu()


if __name__ == "__main__":
    run()
