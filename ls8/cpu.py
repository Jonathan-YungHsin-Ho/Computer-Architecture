"""CPU functionality."""

import sys


ADD = 0b10100000
AND = 0b10101000
CALL = 0b1010000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
INT = 0b01010010
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110
LD = 0b10000011
LDI = 0b10000010
MOD = 0b10100100
MUL = 0b10100010
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = 0
        self.ie = 0

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self, program):
        """Load a program into memory."""
        try:
            address = 0
            with open(program) as f:
                for line in f:
                    line = line.split('#')[0]
                    line = line.strip()
                    if line == '':
                        continue
                    instruction = int(line, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print('ERROR: Must have file name')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == 'AND':
            # Perform bitwise-AND on value in register
            self.pc += 2
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                # Set Equal E flag to 1
                pass
            else:
                # Set Equal E flag to 0
                pass
            if self.reg[reg_a] < self.reg[reg_b]:
                # Set Less-than L flag to 1
                pass
            else:
                # Set Less-than L flag to 0
                pass
            if self.reg[reg_a] > self.reg[reg_b]:
                # Set Greater-than G flag to 1
                pass
            else:
                # Set Greater-than G flag to 0
                pass
            self.pc += 3
        elif op == 'DEC':
            self.reg[reg_a] -= 1
            self.pc += 2
        elif op == 'DIV':
            if self.reg[reg_b] == 0:
                # Print error message and halt
                pass
            else:
                self.reg[reg_a] /= self.reg[reg_b]
            self.pc += 3
        elif op == 'INC':
            self.reg[reg_a] += 1
            self.pc += 2
        elif op == 'MOD':
            if self.reg[reg_b] == 0:
                # Print error message and halt
                pass
            else:
                self.reg[reg_a] %= self.reg[reg_b]
            self.pc += 3
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == 'NOT':
            # Perform bitwise-NOT on value in register
            self.pc += 2
        elif op == 'OR':
            # Perform bitwise-OR on value in register
            self.pc += 2
        elif op == 'SHL':
            # Shift value in registerA left by number of bits specified in registerB, filling low bits with 0
            self.pc += 3
        elif op == 'SHR':
            # Shift value in registerA right by number of bits specified in registerB, filling low bits with 0
            self.pc += 3
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 3
        elif op == 'XOR':
            # Perform bitwise-XOR between values in registerA and registerB, storing result in registerA
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == CALL:
                pass
            elif ir == HLT:
                sys.exit(0)
            elif ir == IRET:
                pass
            elif ir == JEQ:
                pass
            elif ir == JGE:
                pass
            elif ir == JGT:
                pass
            elif ir == JLE:
                pass
            elif ir == JLT:
                pass
            elif ir == JMP:
                self.pc = operand_a
                self.pc += 2
            elif ir == JNE:
                pass
            elif ir == LD:
                pass
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == NOP:
                self.pc += 1
            elif ir == POP:
                pass
            elif ir == PRA:
                pass
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 1
            elif ir == PUSH:
                pass
            elif ir == RET:
                pass
            elif ir == ST:
                pass
            elif ir == MUL:
                self.alu(ir, operand_a, operand_b)
            else:
                print(f'Unknown instruction at index {self.pc}')
                sys.exit(1)
