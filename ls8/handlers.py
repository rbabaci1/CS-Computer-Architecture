
import sys
# CPU instructions binary value
LDI, PRN, HALT, MUL, ADD, PUSH, POP, JMP, ST, PRA, IRET, LD, CALL, RET, CMP, JEQ, JNE, AND, OR, XOR = 0b10000010, 0b01000111, 0b00000001, 0b10100010, 0b10100000, 0b01000101, 0b01000110, 0b01010100, 0b10000100, 0b01001000, 0b00010011, 0b10000011, 0b01010000, 0b00010001, 0b10100111, 0b01010101, 0b01010110, 0b10101000, 0b10101010, 0b10101011


def handle_LDI(self, *args):
    reg_num, value, num_operands = args[0], args[1], args[2]
    self.registers[reg_num] = value
    self.PC += num_operands


def handle_PRN(self, *args):
    reg_num, num_operands = args[0], args[2]
    print(" -------------------")
    print(f"| Register_{reg_num} |  {self.registers[reg_num]} |")
    print(" -------------------")
    self.PC += num_operands


def handle_HALT(self, *args):
    self.halted, num_operands = True, args[2]
    self.PC += num_operands
    print(" -------------------")
    print("|    *** HALT ***   |")
    print(" -------------------")


def handle_MUL(self, *args):
    reg_a, reg_b, num_operands = args[0], args[1], args[2]
    self.alu("MUL", reg_a, reg_b)
    self.PC += num_operands


def handle_ADD(self, *args):
    reg_a, reg_b, num_operands = args[0], args[1], args[2]
    self.alu("ADD", reg_a, reg_b)
    self.PC += num_operands


def handle_PUSH(self, *args):
    self.registers[self.SP] -= 1
    valueToPush, num_operands = self.registers[args[0]], args[2]
    self.ram_write(valueToPush, self.registers[self.SP])
    self.PC += num_operands


def handle_POP(self, *args):
    if self.registers[self.SP] == 0xF4:
        print("\n*** THE STACK IS EMPTY. EXITING... TO AVOID UNDERFLOWING ***\n")
        sys.exit(1)

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
    value = self.registers[args[0]]
    print(chr(value)) if value else None
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
    self.interrupts_enabled = True


def handle_LD(self, *args):
    reg_a, reg_b, num_operands = args[0], args[1], args[2]
    value_to_load = self.ram_read(self.registers[reg_b])
    self.registers[reg_a] = value_to_load
    self.PC += num_operands


def handle_CALL(self, *args):
    reg_n, num_operands,  = args[0], args[2]
    self.registers[self.SP] -= 1
    self.ram_write(self.PC + num_operands, self.registers[self.SP])
    self.PC = self.registers[reg_n]


def handle_RET(self, *args):
    self.PC = self.ram_read(self.registers[self.SP])
    self.registers[self.SP] += 1

def handle_CMP(self, *args):
    reg_a, reg_b, num_operands = args[0], args[1], args[2]
    self.alu("CMP", reg_a, reg_b)
    self.PC += num_operands
    
def handle_JEQ(self, *args):
    if self.FL & 1 == 1:
        handle_JMP(self, *args)
    else:
        self.PC += args[2]

def handle_JNE(self, *args):
    if self.FL & 1 == 0:
        handle_JMP(self, *args)
    else:
        self.PC += args[2]
        
def handle_AND(self, *args):
    reg_a, reg_b, num_operands = args[0], args[1], args[2]
    self.alu("AND", reg_a, reg_b)
    self.PC += num_operands
    
def handle_OR(self, *args):
    reg_a, reg_b, num_operands = args[0], args[1], args[2]
    self.alu("OR", reg_a, reg_b)
    self.PC += num_operands
    
def handle_XOR(self, *args):
    reg_a, reg_b, num_operands = args[0], args[1], args[2]
    self.alu("XOR", reg_a, reg_b)
    self.PC += num_operands