from vm.bytecode import *
from vm.utils import eprint


class UnknownInstruction(Exception):
    def __init__(self, err):
        Exception.__init__(self, "Unknown instruction: {}".format(err))


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
        self.global_data = [None] * datasize

        self.ip = entrypoint
        self.sp = -1
        self.fp = None

    def dissassemble(self, opcode):
        if INSTRUCTIONS[opcode].n_operands == 0:
            eprint("%04d: %s" % (self.ip, INSTRUCTIONS[opcode].name))
        elif INSTRUCTIONS[opcode].n_operands == 1:
            eprint("%04d: %s %d" % (
                self.ip, INSTRUCTIONS[opcode].name, self.code[self.ip + 1]))
        elif INSTRUCTIONS[opcode].n_operands == 2:
            eprint(
                "%04d: %s %d %d" % (
                    self.ip, INSTRUCTIONS[opcode].name, self.code[self.ip + 1], self.code[self.ip + 2]))

    def show_stack(self):
        eprint("Stack =\t%s" % str(self.stack[:self.sp + 1]))

    def show_globals(self):
        to_print = ["%04d: %d" % (i, x) for (i, x) in enumerate(self.global_data) if x is not None]
        eprint('-' * 30)
        eprint("\nGlobal Data")
        eprint('\n'.join(to_print))

    def cpu(self):
        while self.ip < len(self.code):
            # Fetch
            opcode = self.code[self.ip]

            if self.trace:
                self.dissassemble(opcode)
            # Move to the operand
            self.ip += 1

            # Decode
            if opcode == HALT:
                if self.trace:
                    self.show_globals()
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
            elif opcode == GLOAD:
                # Get address from code memory
                address = self.code[self.ip]
                self.ip += 1

                # Get value from global memory
                value = self.global_data[address]

                # Store on stack
                self.stack[self.sp] = value
                self.sp += 1

            elif opcode == GSTORE:
                # Get value from top of stack
                top_of_stack_element = self.stack[self.sp]
                self.sp -= 1

                # Store at address specified in code memory
                address = self.code[self.ip]
                self.ip += 1
                self.global_data[address] = top_of_stack_element
            else:
                raise UnknownInstruction(opcode)
            if self.trace:
                self.show_stack()
