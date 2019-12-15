from vm.bytecode import *


class VM:
    def __init__(self, code, entrypoint, datasize, stacksize):
        """

        :param code: Code memory
        :param entrypoint: Main function address
        :param datasize: Size of data
        :param stacksize: Size of stack
        """
        self.datasize = datasize
        self.stacksize = stacksize
        self.code = code
        self.stack = [None] * stacksize
        self.data = [None] * datasize

        self.ip = entrypoint
        self.sp = -1
        self.fp = None

    def cpu(self):
        # Fetch
        opcode = self.code[self.ip]

        # Move to the operand
        self.ip += 1

        # Decode
        if opcode == HALT:
            return
