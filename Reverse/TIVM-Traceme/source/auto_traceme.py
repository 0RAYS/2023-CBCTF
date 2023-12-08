import lib.tri_inst_compiler as tic
import gen_putstr
from secret import flag_traceme as flag
import bin_interface

import random

def make_random(l : list):
    n = len(l)
    for i in range(n - 1):
        k = random.randint(i + 1, n - 1)
        l[i], l[k] = l[k], l[i]

def randomness(s : str):
    rd_pattern = '_RD%d:'
    jmp_pattern = 'jmp %%_RD%d'

    lines = s.rstrip('\n').split('\n')

    header = 'jmp %_RD0'
    tail = rd_pattern % len(lines)

    for i in range(len(lines)):
        line = lines[i]
        lines[i] = '\n'.join([rd_pattern % i, line, jmp_pattern % (i+1)])
    
    make_random(lines)
    return '\n'.join([header, '\n'.join(lines), tail])


putstr_hello = gen_putstr.gen_putstr_tight('Can you catch me?\nCheck flag here:', 0)
putstr_great = gen_putstr.gen_putstr_tight('Great job!', 1)
putstr_wrong = gen_putstr.gen_putstr_tight('Oops. What a pity.', 2)

pattern_check = '''\
get [%%BUF]
chk-jne [%%BUF], #%x, %%_PUT2
'''

script_part_check = '''\
jmp %CHK
BUF:
raw #0
CHK:
'''

_checks = ''.join([pattern_check % x for x in list(flag.encode())])
script_part_check += randomness(_checks)

script = f'''\
jmp %_PUT0
{putstr_hello}
{script_part_check}
jmp %_PUT1
{putstr_great}
jmp %END
{putstr_wrong}
END:
put #0a
'''

if __name__ == "__main__":
    compiler = tic.TriInstCompiler()
    pre_compiled = compiler.ti_precompile(script)

    bytecode = compiler.get_bytecode(pre_compiled)
    open('traceme.tribc', 'w').write(bytecode)

    code = compiler.ti_compile(pre_compiled)
    open('traceme.tricode', 'w').write(str(code))

    bc = bin_interface.mem2bin(code)
    open('traceme.bin', 'wb').write(bc)