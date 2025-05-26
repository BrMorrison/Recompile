from dataclasses import dataclass

"""
Instructions:
- Save <index> <is_match>
- Split <dest1> <dest2>
- Compare <inverse> <char1> <char2>
- Branch <dest> <char1> <char2>
"""

class Instruction:
    """
    Base class for regex instructions
    """
    def code(self) -> str:
        raise AssertionError("Base class should not be used")

@dataclass
class Save(Instruction):
    """
    Saves the location in the input where a match begins or ends.
    If is_match is set, then it also indicates the input matches the pattern.
    """
    index: int
    is_match: bool
    def code(self) -> str:
        return f"Save {self.index} {self.is_match}"

@dataclass
class Split(Instruction):
    """
    Continue execution from two different locations in the program.
    """
    dest1: int
    dest2: int
    def code(self) -> str:
        return f"Split {self.dest1} {self.dest2}"

@dataclass
class Branch(Instruction):
    """
    Jump to a given destination if the current input character is within a given range.
    """
    consume: bool
    inverted: bool
    dest: int
    c_min: int
    c_max: int
    def code(self) -> str:
        c_min = encode_char(self.c_min)
        c_max = encode_char(self.c_max)

        match (self.consume, self.inverted):
            case (True, False):
                return f"Compare {c_min} {c_max}"
            case (True, True):
                return f"InvCompare {c_min} {c_max}"
            case (False, _):
                return f"Branch {c_min} {c_max} {self.dest}"

def encode_char(c: int) -> str:
    '''
    Takes a uint8 and converts it to a printable character, escaping it as necessary for
    whitespace and non-ascii characters.
    '''
    encoded = chr(c)
    if encoded.isascii() and not encoded.isspace() and encoded != '%':
        return encoded
    else:
        return f"%{c}"
