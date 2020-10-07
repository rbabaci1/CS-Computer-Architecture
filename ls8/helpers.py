
import sys


def clear_bit(self, position):
    mask = 1 << position
    self.registers[self.IS] &= ~mask


def stack_cpu_state(self):
    if self.stack_is_empty:
        self.registers[self.SP] = len(self.ram) - 8
        self.stack_is_empty = False

    for i in [self.PC, self.FL, self.registers[:6]]:
        self.registers[self.SP] -= 1
        self.ram_write(i, self.registers[self.SP])


def run_timer_interrupt(self):
    self.registers[self.IS] |= 1  # set bit 0 in the IS
    self.interrupts_enabled = True


def run_keyboard_interrupt(self, e):
    self.registers[self.IS] |= 2
    self.interrupts_enabled = True

    try:
        self.ram_write(ord(e.name), 0xF4)
    except TypeError:
        self.ram_write(0, 0xF4)
        print(e.name)
