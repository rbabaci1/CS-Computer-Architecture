import time


def handle_LDI(self, *args):
    reg_num, value, num_operands = args[0], args[1], args[2]
    self.registers[reg_num] = value
    self.PC += num_operands


def handle_PRN(self, *args):
    reg_num, num_operands = args[0], args[2]
    print(" -------------------")
    print(f"| Register_{reg_num} |   {self.registers[reg_num]}  |")
    print(" -------------------")
    self.PC += num_operands


def handle_HALT(self, *args):
    self.halted, num_operands = True, args[2]
    print("HALT")
    self.PC += num_operands


def handle_MUL(self, *args):
    reg_a, reg_b, num_operands = args[0], args[1], args[2]
    self.alu("MUL", reg_a, reg_b)
    self.PC += num_operands


def handle_ADD(self, *args):
    reg_a, reg_b, num_operands = args[0], args[1], args[2]
    self.alu("ADD", reg_a, reg_b)
    self.PC += num_operands


def handle_PUSH(self, *args):
    # stack starts at last memory index
    if self.stack_is_empty:
        self.registers[self.SP] = len(self.ram) - 8
        self.stack_is_empty = False

    self.registers[self.SP] -= 1
    valueToPush, num_operands = self.registers[args[0]], args[2]
    self.ram_write(valueToPush, self.registers[self.SP])
    self.PC += num_operands


def handle_POP(self, *args):
    reg_to_store_in, num_operands = args[0], args[2]
    value_to_store = self.ram_read(self.registers[self.SP])
    self.registers[reg_to_store_in] = value_to_store
    self.registers[self.SP] += 1
    self.PC += num_operands


def handle_JMP(self, *args):
    reg_to_jump_to = self.registers[args[0]]
    self.PC = reg_to_jump_to


def handle_ST(self, *args):
    value_to_store, num_operands = self.registers[args[1]], args[2]
    address_to_store_at = self.registers[args[0]]
    self.ram_write(value_to_store, address_to_store_at)
    self.PC += num_operands


def handle_PRA(self, *args):
    num_operands = args[2]
    print(chr(self.registers[args[0]]))
    self.PC += num_operands


def handle_IRET(self, *args):
    s_registers = self.ram_read(self.registers[self.SP])
    self.registers[self.SP] += 1
    s_FL = self.ram_read(self.registers[self.SP])
    self.registers[self.SP] += 1
    s_PC = self.ram_read(self.registers[self.SP])
    self.registers[self.SP] += 1

    self.registers = s_registers + self.registers[6:]
    self.FL = s_FL
    self.PC = s_PC
