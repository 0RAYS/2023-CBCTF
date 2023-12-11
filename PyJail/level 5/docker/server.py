WELCOME = '''
 _     _______     _______ _       ____  
| |   | ____\ \   / / ____| |     | ___| 
| |   |  _|  \ \ / /|  _| | |     |___ \ 
| |___| |___  \ V / | |___| |___   ___) |
|_____|_____|  \_/  |_____|_____| |____/ 
                                         
'''

black = ["input", "import", "os", "open", "popen", "system", "read", "_", "'", "\""]

print(WELCOME)

print("Welcome to the JBNRZ's pyjail")
print("Enter your expression and I will evaluate it for you.")
print("Example: ")
print("  input: 1 + 1")
print("  Result: 2")
input_data = input("> ")
if any([i in input_data for i in black]):
    print("Ohhhh, what are you doing???!!!")
    exit(0)
try:
    print("Result: {}".format(eval(input_data)))
except Exception as e:
    print(f"Result: {e}")