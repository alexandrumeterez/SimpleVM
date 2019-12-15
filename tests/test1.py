import sys

sys.path.append('..')

from vm.bytecode import *
from vm.virtualmachine import VM


def run():
    hello = [
        ICONST, 99,
        GSTORE, 0,
        GLOAD, 0,
        PRINT,
        HALT
    ]
    vm = VM(hello, 0, 10, 100)
    vm.cpu()


if __name__ == "__main__":
    run()
