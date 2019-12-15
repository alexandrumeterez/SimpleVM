import sys

sys.path.append('..')

from vm.bytecode import *
from vm.virtualmachine import VM


def run():
    hello = [
        LOAD, -3,  # get n 0
        ICONST, 2,  # put 2 on stack 2
        ILT,  # compare 4
        BRF, 10,  # if false, recurse 5
        ICONST, 1,  # else, put 1 on stack 7
        RET,  # 9

        LOAD, -3,  # take n 10
        LOAD, -3,  # take n to calculate n-1 12
        ICONST, 1,  # put 1 on stack 14
        ISUB,  # now have n-1 on stack 16
        CALL, 0, 1,  # recurse 17
        IMUL,  # 20
        RET,  # 21

        ICONST, 5,  # 22
        CALL, 0, 1,  # 24
        PRINT,  # 27
        HALT

    ]
    vm = VM(hello, 22, 100, 100)
    vm.cpu()


if __name__ == "__main__":
    run()
