"""CPU functionality."""

import sys
import time
import keyboard
import helpers as hp
import handlers as hd


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # initialize the ram with 256 bytes
        self.registers = [0] * 8  # initialize 8 registers
        self.registers[7] = 0xF4  # set R7 to a hex value
        self.halted = False  # CPU not halted yet
        self.address = 0
        self.interrupts_enabled = True
        # internal registers
        self.PC = 0
        self.SP = 7  # stack pointer
        self.IR = None
        self.FL = 0
        self.IM = 5  # interrupt mask
        self.IS = 6  # interrupt status

        self.branch_table = {  # a table to store the helpers for fast lookup
            hd.LDI: hd.handle_LDI,
            hd.PRN: hd.handle_PRN,
            hd.HALT: hd.handle_HALT,
            hd.MUL: hd.handle_MUL,
            hd.ADD: hd.handle_ADD,
            hd.PUSH: hd.handle_PUSH,
            hd.POP: hd.handle_POP,
            hd.JMP: hd.handle_JMP,
            hd.ST: hd.handle_ST,
            hd.PRA: hd.handle_PRA,
            hd.IRET: hd.handle_IRET,
            hd.LD: hd.handle_LD,
            hd.CALL: hd.handle_CALL,
            hd.RET: hd.handle_RET,
            hd.CMP: hd.handle_CMP,
            hd.JEQ: hd.handle_JEQ,
            hd.JNE: hd.handle_JNE,
            hd.AND: hd.handle_AND,
            hd.OR: hd.handle_OR,
            hd.XOR: hd.handle_XOR,
            hd.NOT: hd.handle_NOT,
            hd.SHL: hd.handle_SHL,
            hd.SHR: hd.handle_SHR,
            hd.MOD: hd.handle_MOD,
            hd.ADDI: hd.handle_ADDI,
            hd.INC: hd.handle_INC,
            hd.DEC: hd.handle_DEC
        }

    def load(self, file_name):
        """Load a program into memory."""
        hp.write_program_to_ram(self, file_name)

    def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""
        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        elif op == "CMP":
            hp.set_FL_kth_bit(self, reg_a, reg_b)
        elif op == "AND":
            self.registers[reg_a] = (self.registers[reg_a] & self.registers[reg_b])
        elif op == "OR":
            self.registers[reg_a] = (self.registers[reg_a] | self.registers[reg_b])
        elif op == "XOR":
            self.registers[reg_a] = (self.registers[reg_a] ^ self.registers[reg_b])
        elif op == "NOT":
            self.registers[reg_a] = (~self.registers[reg_a])
        elif op == "SHL":
            self.registers[reg_a] = (self.registers[reg_a] << self.registers[reg_b])
        elif op == "SHR":
            self.registers[reg_a] = (self.registers[reg_a] >> self.registers[reg_b])
        elif op == "MOD":
            if self.registers[reg_b] == 0:
                print("Can't perform a division over 0, second value can't be 0.")
                self.halted = True
            else:
                self.registers[reg_a] = (self.registers[reg_a] % self.registers[reg_b])
        elif op == "ADDI":
            self.registers[reg_a] += reg_b
        elif op == "INC":
            self.registers[reg_a] += 1
        elif op == "DEC":
            self.registers[reg_a] -= 1
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, MAR):
        """should accept the address to read and return the value stored there"""
        if MAR < len(self.ram):
            return self.ram[MAR]

    def ram_write(self, MDR, address):
        """should accept the value to write, and the address to write to"""
        self.ram[address] = MDR

    def handle_keyboard_interrupt(self, k_e):
        hp.run_keyboard_interrupt(self, k_e)

    def run(self):
        """Run the CPU."""
        keyboard.on_press(self.handle_keyboard_interrupt)

        start_time = time.time()
        while not self.halted:
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1:
                hp.run_timer_interrupt(self)
                start_time = time.time()

            if self.interrupts_enabled:
                masked_interrupts = self.registers[self.IM] & self.registers[self.IS]
                for i in range(8):
                    interrupt_happend = ((masked_interrupts >> i) & 1) == 1
                    if interrupt_happend:
                        # disable further interrupts
                        self.interrupts_enabled = False
                        # clear the bit#0 in the IS register
                        hp.clear_bit(self, i)
                        # store the state of the cpu
                        hp.stack_cpu_state(self)
                        # set PC to the interrupt handler address
                        self.PC = self.ram_read(248 + i)
                        break

            if self.address == self.registers[self.SP]:
                print("\n*** THE STACK IS FULL. EXITING... TO AVOID OVERFLOWING ***\n")
                return
            else:   # keep executing instructions as usual
                IR = self.ram_read(self.PC)  # instruction register
                # the number of bytes the instruction has
                num_operands = (IR >> 6) + 1
                operand_a = self.ram_read(self.PC + 1)
                operand_b = self.ram_read(self.PC + 2)
                # Access and call the right function in the branch_table
                self.branch_table[IR](self, operand_a, operand_b, num_operands)
