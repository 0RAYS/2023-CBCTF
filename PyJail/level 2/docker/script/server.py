WELCOME = '''
 _     _______     _______ _       ____  
| |   | ____\ \   / / ____| |     |___ \ 
| |   |  _|  \ \ / /|  _| | |       __) |
| |___| |___  \ V / | |___| |___   / __/ 
|_____|_____|  \_/  |_____|_____| |_____|
                                         
'''

print(WELCOME)

print("Welcome to the JBNRZ's pyjail")
print("Enter your expression and I will evaluate it for you.")
print("Example: ")
print("  input: 1 + 1")
print("  Result: 2")
input_data = input("> ")
try:
    print("Result: {}".format(eval(input_data)))
except Exception as e:
    print(f"Result: {e}")