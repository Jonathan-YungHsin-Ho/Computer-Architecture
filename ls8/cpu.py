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

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == AND:
            # Perform bitwise-AND on value in register
            self.pc += 2
        elif op == CMP:
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
        elif op == DEC:
            self.reg[reg_a] -= 1
            self.pc += 2
        elif op == DIV:
            if self.reg[reg_b] == 0:
                # Print error message and halt
                pass
            else:
                self.reg[reg_a] /= self.reg[reg_b]
            self.pc += 3
        elif op == INC:
            self.reg[reg_a] += 1
            self.pc += 2
        elif op == MOD:
            if self.reg[reg_b] == 0:
                # Print error message and halt
                pass
            else:
                self.reg[reg_a] %= self.reg[reg_b]
            self.pc += 3
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == NOT:
            # Perform bitwise-NOT on value in register
            self.pc += 2
        elif op == OR:
            # Perform bitwise-OR on value in register
            self.pc += 2
        elif op == SHL:
            # Shift value in registerA left by number of bits specified in registerB, filling low bits with 0
            self.pc += 3
        elif op == SHR:
            # Shift value in registerA right by number of bits specified in registerB, filling low bits with 0
            self.pc += 3
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 3
        elif op == XOR:
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
        ir = self.ram[self.pc]
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        while True:
            instruction = self.ram[self.pc]
            # print(instruction)

            if instruction == CALL:
                pass
            elif instruction == HLT:
                sys.exit(0)
            elif instruction == IRET:
                pass
            elif instruction == JEQ:
                pass
            elif instruction == JGE:
                pass
            elif instruction == JGT:
                pass
            elif instruction == JLE:
                pass
            elif instruction == JLT:
                pass
            elif instruction == JMP:
                self.pc = operand_a
                self.pc += 2
            elif instruction == JNE:
                pass
            elif instruction == LD:
                pass
            elif instruction == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction == NOP:
                self.pc += 1
            elif instruction == POP:
                pass
            elif instruction == PRA:
                pass
            elif instruction == PRN:
                print(self.reg[operand_a])
                self.pc += 1
            elif instruction == PUSH:
                pass
            elif instruction == RET:
                pass
            elif instruction == ST:
                pass
            else:
                print(f'Unknown instruction at index {self.pc}')
                sys.exit(1)
