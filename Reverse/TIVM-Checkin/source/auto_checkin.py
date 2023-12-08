import lib.tri_inst_compiler as tic
import gen_putstr
from secret import flag_checkin as flag

s = "Welcome to CBCTF 2023!\nNow guess my lucky number:"
putstr_hello = gen_putstr.gen_putstr_tight(s, 0)
putstr_great = gen_putstr.gen_putstr('Great! Here is your flag:\n%s' % flag, 1)
putstr_wrong = gen_putstr.gen_putstr_tight('wrong', 2)

script = f'''\
jmp %_PUT0
{putstr_hello}
jmp %CHK
BUF:
raw #0
CHK:
get [%BUF]
chk-jne [%BUF], #31, %_PUT2
get [%BUF]
chk-jne [%BUF], #31, %_PUT2
get [%BUF]
chk-jne [%BUF], #34, %_PUT2
get [%BUF]
chk-jne [%BUF], #35, %_PUT2
get [%BUF]
chk-jne [%BUF], #31, %_PUT2
get [%BUF]
chk-jne [%BUF], #34, %_PUT2
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
    # bytecode = compiler.get_bytecode(pre_compiled)
    code = compiler.ti_compile(pre_compiled)

    open('checkin.tricode', 'w').write(str(code))