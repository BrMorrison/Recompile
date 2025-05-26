from . import instruction as inst
import copy

def search(s: str, regex: list[inst.Instruction]) -> str | None:
    matches = []
    execution_step(regex, s, {}, matches, 0, 0)
    longest_match: str | None = None

    for start, end in matches:
        if (longest_match is None) or len(longest_match) < end - start:
            longest_match = s[start:end]

    return longest_match

def execution_step(
        program: list[inst.Instruction],
        s: str,
        save_data: dict[int, int],
        matches: list[tuple[int, int]],
        pc: int,
        sc: int
):
    i = program[pc]
    next_pc = pc+1

    if sc > len(s):
        return
    elif sc == len(s):
        c = 0xFF
    else:
        c = ord(s[sc])
    
    if isinstance(i, inst.Save):
        save_data[i.index] = sc
        if i.is_match:
            matches.append((save_data[i.index-1], save_data[i.index]))
            return
    elif isinstance(i, inst.Split):
        old_data = copy.deepcopy(save_data)
        execution_step(program, s, save_data, matches, i.dest2, sc)
        save_data = old_data
        next_pc = i.dest1
    elif isinstance(i, inst.Branch):
        in_range = c >= i.c_min and c <= i.c_max
        is_match = in_range != i.inverted

        match (i.consume, is_match):
            case (True, False):
                # Failed a consuming Branch, failed to match pattern
                return
            case (True, True):
                sc += 1
            case (False, True):
                next_pc = i.dest
            case (False, False):
                # Nothing wrong with failing on a non-consuming branch
                pass
    else:
        raise AssertionError(f"{i} is not a recognized instruction!")

    execution_step(program, s, save_data, matches, next_pc, sc)
