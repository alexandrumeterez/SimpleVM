from vm.bytecode import *
from vm.utils import eprint


class UnknownInstruction(Exception):
    def __init__(self, err, ip):
        Exception.__init__(self, "Unknown opcode {} at {}".format(err, ip))


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
        self.fp = -1

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
            elif opcode == IADD:
                operand1 = self.stack[self.sp]
                self.sp -= 1
                operand2 = self.stack[self.sp]
                self.sp -= 1
                result = operand1 + operand2
                self.sp += 1
                self.stack[self.sp] = result
            elif opcode == ISUB:
                operand1 = self.stack[self.sp]
                self.sp -= 1
                operand2 = self.stack[self.sp]
                self.sp -= 1
                result = operand2 - operand1
                self.sp += 1
                self.stack[self.sp] = result
            elif opcode == IMUL:
                operand1 = self.stack[self.sp]
                self.sp -= 1
                operand2 = self.stack[self.sp]
                self.sp -= 1
                result = operand1 * operand2
                self.sp += 1
                self.stack[self.sp] = result
            elif opcode == ILT:
                operand1 = self.stack[self.sp]
                self.sp -= 1
                operand2 = self.stack[self.sp]
                self.sp -= 1
                result = (operand1 > operand2)
                self.sp += 1
                self.stack[self.sp] = int(result)
            elif opcode == IEQ:
                operand1 = self.stack[self.sp]
                self.sp -= 1
                operand2 = self.stack[self.sp]
                self.sp -= 1
                result = (operand1 == operand2)
                self.sp += 1
                self.stack[self.sp] = int(result)
            elif opcode == BR:
                branch_to_addr = self.code[self.ip]
                self.ip = branch_to_addr
            elif opcode == BRT:
                branch_to_addr = self.code[self.ip]
                self.ip += 1
                top_of_stack_element = self.stack[self.sp]
                self.sp -= 1
                if top_of_stack_element >= 1:
                    self.ip = branch_to_addr
            elif opcode == BRF:
                branch_to_addr = self.code[self.ip]
                self.ip += 1
                top_of_stack_element = self.stack[self.sp]
                self.sp -= 1
                if top_of_stack_element <= 0:
                    self.ip = branch_to_addr
            elif opcode == LOAD:
                # Load <offset from fp>
                # Loads from offset of fp to stack
                offset = self.code[self.ip]
                self.ip += 1

                # Push on stack
                self.sp += 1
                self.stack[self.sp] = self.stack[self.fp + offset]
            elif opcode == STORE:
                # Stores from stack to offset of fp
                offset = self.code[self.ip]
                self.ip += 1

                self.sp -= 1
                self.stack[self.fp + offset] = self.stack[self.sp]
            elif opcode == POP:
                self.sp -= 1
            elif opcode == CALL:
                # all arguments must be on stack
                # get address of function
                func_addr = self.code[self.ip]
                self.ip += 1
                # get n_args
                n_args = self.code[self.ip]
                self.ip += 1

                # push n_args, current fp and current ip(return addr)
                self.sp += 1
                self.stack[self.sp] = n_args
                self.sp += 1
                self.stack[self.sp] = self.fp
                self.sp += 1
                self.stack[self.sp] = self.ip

                # put fp at current sp(start new stack frame)
                self.fp = self.sp

                # set ip at function address
                self.ip = func_addr
            elif opcode == RET:
                # every function has a return value on stack
                # get return value
                retval = self.stack[self.sp]
                self.sp -= 1

                # set current sp to former sp(where fp points to)
                self.sp = self.fp

                # jump to return address
                self.ip = self.stack[self.sp]
                self.sp -= 1

                # restore fp
                self.fp = self.stack[self.sp]
                self.sp -= 1

                # get n_args
                n_args = self.stack[self.sp]
                self.sp -= 1
                # jump over all args
                self.sp -= n_args

                # put return value on stack
                self.sp += 1
                self.stack[self.sp] = retval

            else:
                raise UnknownInstruction(opcode, self.ip)
            if self.trace:
                self.show_stack()
