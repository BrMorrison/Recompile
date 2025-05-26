#!/bin/env python3

import argparse
import sys

from . import compiler

def main():
    parser = argparse.ArgumentParser(description='A regex compiler for a custom ISA.')
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-r', '--regex', help="The regular expression to compile.")
    input_group.add_argument('-f', '--file', help="A file containing the regex to compile.")
    parser.add_argument(
        '-s', '--asm', action='store_true',
        help="Compile the regex to assembly code without assembling it.")
    parser.add_argument('-o', '--out-file', help="File to write the compiled output to.")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            # Just read the first line
            regex_src = f.read().split('\n')[0]
    else:
        regex_src = args.regex

    # Compile the code
    compiled: str | bytes = ''
    if args.asm:
        compiled = compiler.compile_asm(regex_src)
        file_mode = "w"
    else:
        compiled = compiler.compile_bin(regex_src)
        file_mode = "wb"

    match (args.out_file, args.asm):
        case (None, True):
            out_file = None
        case (None, False):
            out_file = 'out.bin'
        case (f, _):
            out_file = f


    if out_file is None:
        lines = compiled.splitlines()
        print(lines[0])
        for i, inst in enumerate(lines[1:]):
            print(f"{i:3d}: {inst}")
    else:
        with open(out_file, file_mode) as f:
            f.write(compiled)

if __name__ == '__main__':
    main()