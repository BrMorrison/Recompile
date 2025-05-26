from . import syntax, parser, code_gen, instruction, assembler

def compile_regex(regex: str) -> list[instruction.Instruction]:
    # Wrap the regex in a group to allow for extraction of the match.
    parsed = syntax.Group(0, parser.parse(regex))

    # If the regex isn't trying to match from the start of the string, then its equivalent to
    # matching anything (.*) before the provided regex.
    if regex[0] != '$':
        prefix = parser.parse('.*')
        parsed = syntax.Sequence([prefix, parsed])
    
    code = code_gen.compile(parsed)
    return code

def compile_asm(regex: str) -> str:
    '''
    Compile a regex from its string representation to "assembly code"
    '''
    code = compile_regex(regex)
    code_text = '\n'.join(map(lambda inst: inst.code(), code))
    return f"# regex: {regex}\n" + code_text

def compile_bin(regex: str) -> bytes:
    '''
    Compile a regex from its string representation to binary "machine code"
    '''
    code = compile_regex(regex)
    def assemble_to_bytes(i: instruction.Instruction) -> bytes:
        return assembler.assemble(i).to_bytes(length=4)
    return b''.join(map(assemble_to_bytes, code))
