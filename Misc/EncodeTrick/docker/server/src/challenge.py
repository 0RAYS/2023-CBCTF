from ast import (Module, Import, ImportFrom, Call, Expr, Lambda, FunctionDef, AsyncFunctionDef, Del, ClassDef, Is,
                 IsNot, JoinedStr, Try, Expression, Load, ExceptHandler, In, Index, Return, Raise, Continue, Invert,
                 Await, walk)
from subprocess import check_output, DEVNULL


def check(code: Module):
    bad_ast = [
        Import, ImportFrom, Call, Expr, Lambda, FunctionDef, AsyncFunctionDef, Del, ClassDef, Is,
        IsNot, JoinedStr, Try, Expression, Load, ExceptHandler, In, Index, Return, Raise, Continue, Invert, Await
    ]
    for i in walk(code):
        if any([isinstance(i, j) for j in bad_ast]):
            return False
    return True


def challenge(input_code: str):
    code = compile(input_code, "", "exec", flags=1024)
    if check(code):
        input_code += "\n\nprint('result =', result)"
        with open("/tmp/calc.py", "w", encoding="utf-8") as w:
            w.write(input_code)
        cmd = ["timeout", "-s", "KILL", "2", "python", "/tmp/calc.py"]
        try:
            res = check_output(cmd, stderr=DEVNULL).decode().strip()
            return res
        except Exception as e:
            print(e)
            return "Exception"
    else:
        return "What are you doing???"
