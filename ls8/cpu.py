"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # initialize the ram with 256 bytes
        self.ram = [0] * 256
        # initialize 8 registers
        self.registers = [0] * 8
        # internal registers
        self.PC = 0
        self.IR = None
        self.FL = None

    def isKthBitSet(self, n, k):
        if n & (1 << (k - 1)):
            return True

    def getOpcodeHex(self, opcode):
        opcode = hex(opcode)
        return int(opcode[2:])

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

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""
        LDI, PRN, HALT, running = 0b10000010, 0b01000111, 0b00000001, True

        while running:
            IR = self.ram_read(self.PC)
            # identifier = (1 << 4) - 1 & IR
            # num_operands = IR >> 6
            # isALU = self.isKthBitSet(IR, 6)
            # setsPC = self.isKthBitSet(IR, 5)
            # opcode = self.getOpcodeHex(IR)

            if IR == LDI:  # LDI, set the specified register to a specific value
                reg_num = self.ram_read(self.PC + 1)
                value = self.ram_read(self.PC + 2)
                self.registers[reg_num] = value
                print("LDI")
                self.PC += 3

            elif IR == PRN:  # PRN, Print numeric value stored in a given register
                reg_num = self.ram_read(self.PC + 1)
                print(f"R{reg_num} has value of {self.registers[reg_num]}.")
                self.PC += 2

            elif IR == HALT:  # HALT
                print("HALT")
                running = False

    def ram_read(self, MAR):
        """should accept the address to read and return the value stored there"""
        return self.ram[MAR]

    def ram_write(self, MDR, address):
        """should accept the value to write, and the address to write to"""
        self.ram[address] = MDR
