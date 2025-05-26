from . import instruction as inst

from functools import singledispatch
from enum import IntEnum

class Opcode(IntEnum):
    Branch = 0b00
    Compare = 0b01
    Split = 0b10
    Save = 0b11

_opcode_shift = 29
_save_index_shift = 16 # This one can be wherever
_match_shift = 28
_inverted_shift = 28
_dest_shift = 16
_dest2_shift = 4
_char_min_shift = 8
_char_max_shift = 0

# Returns a 32-bit number
@singledispatch
def assemble(val) -> int:
    raise AssertionError(f"Unexpected type for val {val.type}")

@assemble.register
def _(val: inst.Save) -> int:
    asm = (Opcode.Save.value << _opcode_shift) | (int(val.is_match) << _match_shift) \
        | (val.index << _save_index_shift)
    return asm & 0xFFFF_FFFF

@assemble.register
def _(val: inst.Split) -> int:
    asm = (Opcode.Split.value << _opcode_shift) | (val.dest1 << _dest_shift) | (val.dest2 << _dest2_shift)
    return asm & 0xFFFF_FFFF

@assemble.register
def _(val: inst.Compare) -> int:
    asm = (Opcode.Compare.value << _opcode_shift) | (int(val.inverted) << _inverted_shift) \
        | (val.c_min << _char_min_shift) \
        | (val.c_max << _char_max_shift)
    return asm & 0xFFFF_FFFF

@assemble.register
def _(val: inst.Branch) -> int:
    asm = (Opcode.Branch.value << _opcode_shift) | (val.dest << _dest_shift) \
        | (val.c_min << _char_min_shift) \
        | (val.c_max << _char_max_shift)
    return asm & 0xFFFF_FFFF
