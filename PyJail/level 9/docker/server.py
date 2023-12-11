import ast

WELCOME = '''
 _     _______     _______ _        ___  
| |   | ____\ \   / / ____| |      / _ \ 
| |   |  _|  \ \ / /|  _| | |     | (_) |
| |___| |___  \ V / | |___| |___   \__, |
|_____|_____|  \_/  |_____|_____|    /_/ 
                                         
'''


def verify_ast_secure(m):
    for x in ast.walk(m):
        if type(x) in [ast.Import, ast.ImportFrom, ast.Call, ast.Expr, ast.Add, ast.Lambda, ast.FunctionDef, ast.AsyncFunctionDef, ast.Sub, ast.Mult, ast.Div, ast.Del]:
            print(f"ERROR: Banned statement {x}")
            return False
    return True


def exexute_code(my_source_code):
    print("Pls input your code: (last line must contain only --CBCTF)")
    while True:
        line = input() + "\n"
        if line.startswith("--CBCTF"):
            break
        my_source_code += line

    tree_check = compile(my_source_code, "input_code.py", 'exec', flags=ast.PyCF_ONLY_AST)
    if verify_ast_secure(tree_check):
        print("check is passed!now the result is:")
        compiled_code = compile(my_source_code, "input_code.py", 'exec')
        exec(compiled_code)


if __name__ == '__main__':
    print(WELCOME)
    print("=================================================================================================")
    print("==           Welcome to the JBNRZ's pyjail level9,It's AST challenge                       ==")
    print("==           Menu list:                                                                        ==")
    print("==             [G]et the blacklist AST                                                         ==")
    print("==             [E]xecute the python code                                                       ==")
    print("==             [Q]uit jail challenge                                                           ==")
    print("=================================================================================================")
    ans = (input().strip()).lower()
    if ans == 'g':
        print("=================================================================================================")
        print("==        Black List AST:                                                                      ==")
        print("==                       'Import,ImportFrom,Call,Expr,Add,Lambda,FunctionDef,AsyncFunctionDef  ==")
        print("==                        Sub,Mult,Div,Del'                                                    ==")
        print("=================================================================================================")
    elif ans == 'e':
        my_source_code = ""
        exexute_code(my_source_code)
    elif ans == 'q':
        print("Bye")
        quit()
    else:
        print("Unknown options!")
        quit()