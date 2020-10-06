"""CPU functionality."""

import sys

LDI, PRN, HALT, MUL, ADD, PUSH, POP, JMP = 0b10000010, 0b01000111, 0b00000001, 0b10100010, 0b10100000, 0b01000101, 0b01000110, 0b01010100


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # initialize the ram with 256 bytes
        self.registers = [0] * 8  # initialize 8 registers
        self.registers[7] = 0xF4  # set R7 to a hex value
        self.halted = False  # CPU not halted yet
        self.address = 0
        self.stack_is_empty = True
        # internal registers
        self.PC = 0
        self.SP = 7  # stack pointer
        self.IR = None
        self.FL = None
        self.branch_table = {  # a table to store the helpers for fast lookup
            LDI: self.handle_LDI,
            PRN: self.handle_PRN,
            HALT: self.handle_HALT,
            MUL: self.handle_MUL,
            ADD: self.handle_ADD,
            PUSH: self.handle_PUSH,
            POP: self.handle_POP,
            JMP: self.handle_JMP
        }

    def isKthBitSet(self, n, k):
        if n & (1 << (k - 1)):
            return True

    def getOpcodeHex(self, opcode):
        opcode = hex(opcode)
        return int(opcode[2:])

    def load(self, program):
        """Load a program into memory."""
        for instruction in program:
            self.ram_write(instruction, self.address)
            self.address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def handle_LDI(self, *args):
        reg_num, value = args[0], args[1]
        self.registers[reg_num] = value
        # print("LDI")

    def handle_PRN(self, *args):
        reg_num = args[0]
        print(" -------------------")
        print(f"| Register_{reg_num} |   {self.registers[reg_num]}  |")
        print(" -------------------")

    def handle_HALT(self, *args):
        self.halted = True
        # print("HALT")

    def handle_MUL(self, *args):
        reg_a, reg_b = args[0], args[1]
        self.alu("MUL", reg_a, reg_b)

    def handle_ADD(self, *args):
        reg_a, reg_b = args[0], args[1]
        self.alu("ADD", reg_a, reg_b)

    def handle_PUSH(self, *args):
        # stack starts at last memory index
        if self.stack_is_empty:
            self.registers[self.SP] = len(self.ram)
            self.stack_is_empty = False

        self.registers[self.SP] -= 1
        valueToPush = self.registers[args[0]]
        self.ram_write(valueToPush, self.registers[self.SP])

    def handle_POP(self, *args):
        reg_to_store_in = args[0]
        value_to_store = self.ram_read(self.registers[self.SP])
        self.registers[reg_to_store_in] = value_to_store
        self.registers[self.SP] += 1

    def handle_JMP(self, *args):
        reg_to_jump_to = self.registers[args[0]]
        self.PC = reg_to_jump_to

    def run(self):
        """Run the CPU."""

        while not self.halted:
            if self.address == self.registers[self.SP]:
                print("*** IT'S TIME TO EXIT, THE STACK IS ABOUT TO OVER FLOW ***")
                return
            IR = self.ram_read(self.PC)  # instruction register
            # the number of bytes the instruction has
            num_operands = (IR >> 6) + 1
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            self.branch_table[IR](operand_a, operand_b)
            self.PC += num_operands

    def ram_read(self, MAR):
        """should accept the address to read and return the value stored there"""
        if MAR < len(self.ram):
            return self.ram[MAR]

    def ram_write(self, MDR, address):
        """should accept the value to write, and the address to write to"""
        self.ram[address] = MDR
