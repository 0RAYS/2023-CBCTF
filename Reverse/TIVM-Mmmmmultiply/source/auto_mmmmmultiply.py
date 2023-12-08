import lib.tri_inst_compiler as tic
import gen_putstr
from secret import flag_mmmmmultiply as flag
import numpy as np
import random
import bin_interface

def get_rand_mat(n : int):
    result = []
    for i in range(n):
        t = []
        for j in range(n):
            t.append(random.randint(0, 7))
        result.append(t)
    return np.mat(result)

target_n = 6
mat = get_rand_mat(target_n)

rank = np.linalg.matrix_rank(mat)

print('生成矩阵')
print(mat)
print('秩：', end='')
print(rank)

assert(target_n == rank)
assert(len(flag) == target_n * target_n)

def get_flag_mat(flag : str, n : int):
    b = flag.encode()
    result = []
    for i in range(0, n * n, n):
        result.append(list(b[i:i+n]))
    return np.mat(result)

flag_mat = get_flag_mat(flag, target_n)

print('flag矩阵')
print(flag_mat)

check_mat = np.matmul(flag_mat, mat)

print('check矩阵')
print(check_mat)

def gen_check_subs(num : int, arg1 : str, arg2 : int):
    pattern = 'sub [%%%s], [%%INP+%x]\n'
    return (pattern % (arg1, arg2)) * num

def gen_check_part(inp_line : int, key : list[int], ans : int, number : int) -> str:
    tag_ckp = '_CKP%d' % number
    tag_ckpbuf = '_CKPBUF%d' % number

    script_check = f'''\
jmp %{tag_ckp}
{tag_ckpbuf}:
raw #0
{tag_ckp}:
'''

    script_buf = [script_check]
    for i in range(len(key)):
        t = gen_check_subs(key[i], tag_ckpbuf, inp_line * len(key) + i)
        script_buf.append(t)

    rev_ans = '%x' % (0x100000000 - ans)

    tail = f'''\
chk-jne [%{tag_ckpbuf}], #{rev_ans}, %_PUT2
'''
    
    script_buf.append(tail)
    return ''.join(script_buf)


script_input_buf = 'INP:\n' + 'raw #0\n' * (target_n * target_n)
script_input = '\n'.join(['get [%%INP+%x]' % x for x in range(target_n * target_n)])

putstr_hello = gen_putstr.gen_putstr_tight("Mixed with something math and something magic.\nGimme flag:", 0)
putstr_great = gen_putstr.gen_putstr_tight("Yes! Yes! Yes!", 1)
putstr_wrong = gen_putstr.gen_putstr_tight("No. No. No.", 2)

script_check = []
for j in range(target_n):
    for i in range(target_n):
        key = [mat[x, i] for x in range(target_n)]
        t = gen_check_part(j, key, check_mat[j, i], j * target_n + i)
        script_check.append(t)
script_check = ''.join(script_check)

script = f'''\
jmp %_PUT0
{script_input_buf}
{putstr_hello}
{script_input}
{script_check}
jmp %_PUT1
{putstr_great}
jmp %END
{putstr_wrong}
END:
put #0a
'''

if __name__ == "__main__":
    open('mmmmmultiply.src', 'w').write(script)

    compiler = tic.TriInstCompiler()
    pre_compiled = compiler.ti_precompile(script)

    bytecode = compiler.get_bytecode(pre_compiled)
    open('mmmmmultiply.tribc', 'w').write(bytecode)

    code = compiler.ti_compile(pre_compiled)
    open('mmmmmultiply.tricode', 'w').write(str(code))

    bc = bin_interface.mem2bin(code)
    open('mmmmmultiply.bin', 'wb').write(bc)