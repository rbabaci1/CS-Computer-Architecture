def write_program_to_ram(self, file_name):
    try:
        with open(f"examples/{file_name}") as fp:
            for l in fp:
                binary_string = l.partition("#")[0].strip()
                if len(binary_string):
                    self.ram_write(int(binary_string, 2), self.address)
                    self.address += 1 
    except FileNotFoundError:
        print("*** THE SPECIFIED FILE NAME DOESN'T EXIST ***")

def clear_bit(self, position):
    mask = 1 << position
    self.registers[self.IS] &= ~mask
    
def set_FL_kth_bit(self, reg_a, reg_b):
    if self.registers[reg_a] == self.registers[reg_b]:
        self.FL = ((1 << 0) | self.FL)
    elif self.registers[reg_a] > self.registers[reg_b]:
        self.FL = ((1 << 1) | self.FL)
    else:
        self.FL = ((1 << 2) | self.FL)

def stack_cpu_state(self):
    for i in [self.PC, self.FL, self.registers[:6]]:
        self.registers[self.SP] -= 1
        self.ram_write(i, self.registers[self.SP])


def run_timer_interrupt(self):
    self.registers[self.IS] |= 1  # set bit 0 in the IS


def run_keyboard_interrupt(self, e):
    self.registers[self.IS] |= 2
    try:
        self.ram_write(ord(e.name), 0xF4)
    except TypeError:
        self.ram_write(0, 0xF4)
        print(e.name)
