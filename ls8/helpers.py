def handle_LDI(self, *args):
    reg_num, value = args[0], args[1]
    self.registers[reg_num] = value


def handle_PRN(self, *args):
    reg_num = args[0]
    print(" -------------------")
    print(f"| Register_{reg_num} |   {self.registers[reg_num]}  |")
    print(" -------------------")


def handle_HALT(self, *args):
    self.halted = True
    print("HALT")


def handle_MUL(self, *args):
    reg_a, reg_b = args[0], args[1]
    self.alu("MUL", reg_a, reg_b)


def handle_ADD(self, *args):
    reg_a, reg_b = args[0], args[1]
    self.alu("ADD", reg_a, reg_b)


def handle_PUSH(self, *args):
    # stack starts at last memory index
    if self.stack_is_empty:
        self.registers[self.SP] = len(self.ram) - 8
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


def handle_ST(self, *args):
    value_to_store = self.registers[args[1]]
    address_to_store_at = self.registers[args[0]]
    self.ram_write(value_to_store, address_to_store_at)


def handle_PRA(self, *args):
    print(chr(self.registers[args[0]]))
