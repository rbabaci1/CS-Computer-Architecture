"""CPU functionality."""

import sys
import time
import threading
from helpers import handle_HALT, handle_ADD, handle_LDI, handle_POP, handle_MUL, handle_JMP, handle_PUSH, handle_PRN, handle_PRA, handle_ST, handle_IRET

LDI, PRN, HALT, MUL, ADD, PUSH, POP, JMP, ST, PRA, IRET = 0b10000010, 0b01000111, 0b00000001, 0b10100010, 0b10100000, 0b01000101, 0b01000110, 0b01010100, 0b10000100, 0b01001000, 0b00010011


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
        self.IM = 5  # interrupt mask
        self.IS = 6  # interrupt status
        self.interrupts_enabled = False

        self.branch_table = {  # a table to store the helpers for fast lookup
            LDI: handle_LDI,
            PRN: handle_PRN,
            HALT: handle_HALT,
            MUL: handle_MUL,
            ADD: handle_ADD,
            PUSH: handle_PUSH,
            POP: handle_POP,
            JMP: handle_JMP,
            ST: handle_ST,
            PRA: handle_PRA,
            IRET: handle_IRET
        }

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

    def ram_read(self, MAR):
        """should accept the address to read and return the value stored there"""
        if MAR < len(self.ram):
            return self.ram[MAR]

    def ram_write(self, MDR, address):
        """should accept the value to write, and the address to write to"""
        self.ram[address] = MDR

    def clear_bit(self):
        mask = 1 << 0
        self.registers[self.IS] &= ~mask

    def stack_cpu_state(self):
        if self.stack_is_empty:
            self.registers[self.SP] = len(self.ram) - 8
            self.stack_is_empty = False

        for i in [self.PC, self.FL, self.registers[:6]]:
            self.registers[self.SP] -= 1
            self.ram_write(i, self.registers[self.SP])

    def run(self):
        """Run the CPU."""
        start_time = time.time()

        while not self.halted:
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1:
                self.registers[self.IS] |= 1  # set bit 0 in the IS
                self.interrupts_enabled = True
                start_time = time.time()
                print(self.ram)

            if self.interrupts_enabled:
                masked_interrupts = self.registers[self.IM] & self.registers[self.IS]

                for i in range(8):
                    interrupt_happend = ((masked_interrupts >> i) & 1) == 1
                    if interrupt_happend:
                        # disable further interrupts
                        self.interrupts_enabled = False
                        # clear the bit#0 in the IS register
                        self.clear_bit()
                        # store the state of the cpu
                        self.stack_cpu_state()
                        # set PC to the interrupt handler address
                        self.PC = self.ram_read(248)
                        break

            if self.address == self.registers[self.SP]:
                print("*** IT'S TIME TO EXIT, THE STACK IS ABOUT TO OVER FLOW ***")
                return
            IR = self.ram_read(self.PC)  # instruction register
            # the number of bytes the instruction has
            num_operands = (IR >> 6) + 1
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            self.branch_table[IR](self, operand_a, operand_b, num_operands)
