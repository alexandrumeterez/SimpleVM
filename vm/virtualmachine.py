from vm.bytecode import *
from vm.utils import eprint


class VM:
    def __init__(self, code, entrypoint, datasize, stacksize, trace=True):
        """

        :param code: Code memory
        :param entrypoint: Main function address
        :param datasize: Size of data
        :param stacksize: Size of stack
        """
        self.trace = trace
        self.datasize = datasize
        self.stacksize = stacksize
        self.code = code
        self.stack = [None] * stacksize
        self.data = [None] * datasize

        self.ip = entrypoint
        self.sp = -1
        self.fp = None

    def cpu(self):
        opcode = None  # Init opcode

        while self.ip < len(self.code):
            # Fetch
            opcode = self.code[self.ip]

            if self.trace:
                eprint("%04d: %s" % (self.ip, OPCODES[opcode]))

            # Move to the operand
            self.ip += 1

            # Decode
            if opcode == HALT:
                return
            elif opcode == ICONST:
                # Get operand from code memory
                operand = self.code[self.ip]
                self.ip += 1

                # Push operand on stack
                self.sp += 1
                self.stack[self.sp] = operand
            elif opcode == PRINT:
                # Get top of stack
                top_of_stack_element = self.stack[self.sp]
                self.sp -= 1

                # Print it
                print(top_of_stack_element)

        opcode = self.code[self.ip]
