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
        # set R7 to a hex value
        self.registers[7] = 0xF4
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

    def validate_arguments(self, args):
        if len(args) < 2:
            print("\t*******************************************")
            print(f"PLEASE SPECIFY THE FILE NAME TO LOAD AS THE SECOND ARGUMENT")
            print("\t*******************************************")
            sys.exit(1)
        elif len(args) >= 2:
            file_name = args[1]
            if file_name[:9] != "examples/":
                print("\t*******************************************")
                print(f"\t   PLEASE SPECIFY THE CORRECT FOLDER NAME")
                print("\t*******************************************")
                sys.exit(1)
        return args[1]

    def generate_values(self, file_lines):
        values = []
        for l in file_lines:
            binary_string = l.partition("#")[0].strip()
            if len(binary_string):
                values.append(int(binary_string, 2))
        return values

    def load(self):
        """Load a program into memory."""

        address = 0
        file_name = self.validate_arguments(sys.argv)

        with open(file_name) as f:
            lines = f.readlines()

        program = self.generate_values(lines)
        print(program)
        sys.exit(1)

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
        LDI, PRN, HALT, running = 0b0010, 0b0111, 0b0001, True

        while running:
            IR = self.ram_read(self.PC)  # instruction register
            II = (1 << 4) - 1 & IR  # instruction identifier
            num_operands = IR >> 6  # the number of bytes the instruction has
            # isALU = self.isKthBitSet(IR, 6)
            # setsPC = self.isKthBitSet(IR, 5)

            if II == LDI:  # LDI, set the specified register to a specific value
                reg_num = self.ram_read(self.PC + 1)
                value = self.ram_read(self.PC + 2)
                self.registers[reg_num] = value
                self.PC += num_operands + 1
                print("LDI")

            elif II == PRN:  # PRN, Print numeric value stored in a given register
                reg_num = self.ram_read(self.PC + 1)
                print(f"R{reg_num} has value of {self.registers[reg_num]}.")
                self.PC += num_operands + 1

            elif II == HALT:  # HALT
                running = False
                print("HALT")

    def ram_read(self, MAR):
        """should accept the address to read and return the value stored there"""
        return self.ram[MAR]

    def ram_write(self, MDR, address):
        """should accept the value to write, and the address to write to"""
        self.ram[address] = MDR
