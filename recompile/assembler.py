from . import instruction as inst

from functools import singledispatch
from enum import IntEnum

class Opcode(IntEnum):
    Branch = 0b00
    Split = 0b01
    Save = 0b10

_opcode_shift = 30

'''
===============================================
Branch <inv> <cons> <dest> <c_min> <c_max>
-----------------------------------------------
| 31:30 | 29  |  28  | 27:16 | 15:8  |  7:0   |
+-------+-----+------+-------+-------+--------+
| 0b00  | inv | cons | dest  | c_min | c_max  |
-----------------------------------------------
'''
_inverted_shift = 29
_consume_shift = 28
_dest_shift = 16
_char_min_shift = 8
_char_max_shift = 0

'''
===============================================
Split <dest1> <dest2>
-----------------------------------------------
| 31:30 |  29:28   | 27:16 | 15:4  |   3:0    |
+-------+----------+-------+-------+----------+
| 0b01  | reserved | dest1 | dest2 | reserved |
-----------------------------------------------
'''
_dest1_shift = _dest_shift
_dest2_shift = 4

'''
===============================================
Save <match> <index>
-----------------------------------------------
| 31:30 |  29   |  28:22   | 21:16 |   15:0   |
+-------+-------+----------+-------+----------+
| 0b10  | match | reserved | index | reserved |
-----------------------------------------------
'''
_match_shift = 29
_save_index_shift = 16

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
    asm = (Opcode.Split.value << _opcode_shift) | (val.dest1 << _dest1_shift) \
        | (val.dest2 << _dest2_shift)
    return asm & 0xFFFF_FFFF

@assemble.register
def _(val: inst.AluOp) -> int:
    asm = (Opcode.Branch.value << _opcode_shift) | (int(val.inverted) << _inverted_shift) \
        | (int(val.consume) << _consume_shift) | (val.dest << _dest_shift) \
        | (val.c_min << _char_min_shift) | (val.c_max << _char_max_shift)
    return asm & 0xFFFF_FFFF
