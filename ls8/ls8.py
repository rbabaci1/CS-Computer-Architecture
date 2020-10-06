#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU


def generate_program(file_name):
    try:
        with open(f"examples/{file_name}") as fp:
            program = []
            for l in fp:
                binary_string = l.partition("#")[0].strip()
                if len(binary_string):
                    program.append(int(binary_string, 2))
            return program
    except FileNotFoundError:
        print(f"*** THE SPECIFIED FILE NAME DOESN'T EXIST ***")


def main(argv):
    """MAIN"""
    if len(argv) != 2:
        print(
            f"*** PLEASE SPECIFY THE FILE NAME TO LOAD AS THE SECOND ARGUMENT ***"
        )
        return 1

    cpu = CPU()

    program = generate_program(argv[1])
    if not program:
        return 1

    cpu.load(program)
    cpu.run()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
