"""CPU functionality."""

import sys

from datetime import datetime

ADD = 0b10100000
# AND = 0b10101000
CALL = 0b1010000
# CMP = 0b10100111
DEC = 0b01100110
# DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
# INT = 0b01010010
IRET = 0b00010011
# JEQ = 0b01010101
# JGE = 0b01011010
# JGT = 0b01010111
# JLE = 0b01011001
# JLT = 0b01011000
JMP = 0b01010100
# JNE = 0b01010110
# LD = 0b10000011
LDI = 0b10000010
# MOD = 0b10100100
MUL = 0b10100010
# NOP = 0b00000000
# NOT = 0b01101001
# OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
# SHL = 0b10101100
# SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
# XOR = 0b10101011

IM = 5
IS = 6
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[SP] = 0xF4
        self.fl = 0
        self.ie = 0

        self.interrupts_enabled = True
        self.start_time = datetime.now()

        self.branchtable = {
            CALL: self.handle_call,
            HLT: self.handle_hlt,
            # INT: self.handle_int,
            IRET: self.handle_iret,
            # JEQ: self.handle_jeq,
            # JGE: self.handle_jge,
            # JGT: self.handle_jgt,
            # JLE: self.handle_jle,
            # JLT: self.handle_jlt,
            JMP: self.handle_jmp,
            # JNE: self.handle_jne,
            # LD: self.handle_ld,
            LDI: self.handle_ldi,
            # MUL: self.handle_mul,
            # NOP: self.handle_nop,
            POP: self.handle_pop,
            PRA: self.handle_pra,
            PRN: self.handle_prn,
            PUSH: self.handle_push,
            RET: self.handle_ret,
            ST: self.handle_st,
            ADD: self.alu_handle_add,
            # AND: self.alu_handle_and,
            # CMP: self.alu_handle_cmp,
            DEC: self.alu_handle_dec,
            # DIV: self.alu_handle_div,
            INC: self.alu_handle_inc,
            # MOD: self.alu_handle_mod,
            MUL: self.alu_handle_mul,
            # NOT: self.alu_handle_not,
            # OR: self.alu_handle_or,
            # SHL: self.alu_handle_shl,
            # SHR: self.alu_handle_shr,
            SUB: self.alu_handle_sub,
            # XOR: self.alu_handle_xor,
        }

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
                    self.ram_write(instruction, address)
                    address += 1
        except FileNotFoundError:
            print('ERROR: Must have valid file name')
            sys.exit(2)

    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == ADD:
    #         self.reg[reg_a] += self.reg[reg_b]
    #     else:
    #         raise Exception("Unsupported ALU operation")

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
            self.timer_interrupt()
            self.check_interrupts()

            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            operand_count = ir >> 6
            instruction_length = operand_count + 1

            # alu_op = ir >> 5 & 0b001
            sets_pc = ir >> 4 & 0b0001

            self.branchtable[ir](operand_a, operand_b)

            if not sets_pc:
                self.pc += instruction_length

    # Interrupt Methods

    def timer_interrupt(self):
        seconds_elapsed = (datetime.now() - self.start_time).total_seconds()
        if seconds_elapsed >= 1:
            self.reg[IS] |= 0b00000001
            self.start_time = datetime.now()

    def check_interrupts(self):
        if self.interrupts_enabled:
            masked_interrupts = self.reg[IM] & self.reg[IS]

            for i in range(8):
                interrupt_happened = ((masked_interrupts >> i) & 1) == 1
                if interrupt_happened:
                    # Disable further interrupts
                    self.interrupts_enabled = False

                    # Clear bit in IS register
                    # # Update to be bit-specific
                    self.reg[IS] = 0

                    # Push PC register on the stack
                    self.helper_push(self.pc)

                    # Push FL register on the stack
                    self.helper_push(self.fl)

                    # Push registers R0-R6 on the stack in that order
                    for j in range(7):
                        self.helper_push(self.reg[j])

                    # Look up vector from interrupt vector table
                    vector = 0xF8 + i

                    # set PC to vector
                    self.pc = self.ram_read(vector)

                    break

    # Helper Methods

    def helper_push(self, value):
        self.reg[SP] -= 1
        self.ram_write(value, self.reg[SP])

    # General Instructions

    def handle_call(self, a, b):
        # Decrement SP
        self.reg[SP] -= 1

        # Push return address on stack
        return_address = self.pc + 2
        self.ram_write(return_address, self.reg[SP])

        # Set PC to value in register
        reg_num = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_num]

    def handle_hlt(self, *_):
        sys.exit(0)

    # def handle_int(self, a, b):
    #     pass

    def handle_iret(self, *_):
        # Pop registers R6-R0 off stack in that order
        for i in range(6, -1, -1):
            self.handle_pop(i, _)

        # Pop FL register off stack
        fl_reg = self.ram_read(self.reg[SP])
        self.fl = fl_reg
        self.reg[SP] += 1

        # Pop return address off stack and store in PC
        return_addr = self.ram_read(self.reg[SP])
        self.pc = return_addr
        self.reg[SP] += 1

        # Re-enable interrupts
        self.interrupts_enabled = True

    # def handle_jeq(self, a, b):
    #     pass

    # def handle_jge(self, a, b):
    #     pass

    # def handle_jgt(self, a, b):
    #     pass

    # def handle_jle(self, a, b):
    #     pass

    # def handle_jlt(self, a, b):
    #     pass

    def handle_jmp(self, reg_num, _):
        self.pc = self.reg[reg_num]

    # def handle_jne(self, a, b):
    #     pass

    # def handle_ld(self, a, b):
    #     pass

    def handle_ldi(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b

    # def handle_nop(self, a, b):
    #     pass

    def handle_pop(self, reg_num, _):
        # Get value from address pointed to by SP
        val = self.ram_read(self.reg[SP])

        # Copy to given register
        self.reg[reg_num] = val

        # Increment SP
        self.reg[SP] += 1

    def handle_pra(self, reg_num, _):
        print(chr(self.reg[reg_num]))

    def handle_prn(self, reg_num, _):
        print(self.reg[reg_num])

    def handle_push(self, reg_num, _):
        self.helper_push(self.reg[reg_num])

    def handle_ret(self, *_):
        # Pop return address off stack and store it on PC
        self.pc = self.ram_read(self.reg[SP])
        self.reg[SP] += 1

    def handle_st(self, reg_a, reg_b):
        val = self.reg[reg_b]
        address = self.reg[reg_a]
        self.ram_write(val, address)

    # ALU Instructions

    def alu_handle_add(self, reg_a, reg_b):
        self.reg[reg_a] += self.reg[reg_b]

    # def alu_handle_and(self, a, b):
    #     # Perform bitwise-AND on value in register
    #     pass

    # def alu_handle_cmp(self, a, b):
    #     if self.reg[a] == self.reg[b]:
    #         # Set Equal E flag to 1
    #         pass
    #     else:
    #         # Set Equal E flag to 0
    #         pass
    #     if self.reg[a] < self.reg[b]:
    #         # Set Less-than L flag to 1
    #         pass
    #     else:
    #         # Set Less-than L flag to 0
    #         pass
    #     if self.reg[a] > self.reg[b]:
    #         # Set Greater-than G flag to 1
    #         pass
    #     else:
    #         # Set Greater-than G flag to 0
    #         pass

    def alu_handle_dec(self, reg_num, _):
        self.reg[reg_num] -= 1

    # def alu_handle_div(self, a, b):
    #     if self.reg[reg_b] == 0:
    #         # Print error message and halt
    #         pass
    #     else:
    #         self.reg[reg_a] /= self.reg[reg_b]

    def alu_handle_inc(self, reg_num, _):
        self.reg[reg_num] += 1

    # def alu_handle_mod(self, a, b):
    #     if self.reg[reg_b] == 0:
    #         # Print error message and halt
    #         pass
    #     else:
    #         self.reg[reg_a] %= self.reg[reg_b]

    def alu_handle_mul(self, reg_a, reg_b):
        self.reg[reg_a] *= self.reg[reg_b]

    # def alu_handle_not(self, a, b):
    #     # Perform bitwise-NOT on value in register
    #     pass

    # def alu_handle_or(self, a, b):
    #     # Perform bitwise-OR on value in register
    #     pass

    # def alu_handle_shl(self, a, b):
    #     # Shift value in registerA left by number of bits specified in registerB, filling low bits with 0
    #     pass

    # def alu_handle_shr(self, a, b):
    #     # Shift value in registerA right by number of bits specified in registerB, filling low bits with 0
    #     pass

    def alu_handle_sub(self, reg_a, reg_b):
        self.reg[reg_a] -= self.reg[reg_b]

    # def alu_handle_xor(self, a, b):
    #     # Perform bitwise-XOR between values in registerA and registerB, storing result in registerA
    #     pass
