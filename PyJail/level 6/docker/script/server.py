from string import ascii_letters


WELCOME = '''
 _     _______     _______ _        __   
| |   | ____\ \   / / ____| |      / /_  
| |   |  _|  \ \ / /|  _| | |     | '_ \ 
| |___| |___  \ V / | |___| |___  | (_) |
|_____|_____|  \_/  |_____|_____|  \___/ 
                                         
'''

print(WELCOME)
print("Welcome to the JBNRZ's pyjail")
print("Enter your expression and I will evaluate it for you.")
print("Example: ")
print("  input: 1 + 1")
print("  Result: 2")
input_data = input("> ")
if any([i in ascii_letters for i in input_data]):
    print("Ohhhh, what are you doing???!!!")
    exit(0)
try:
    print("Result: {}".format(eval(input_data)))
except Exception as e:
    print(f"Result: {e}")