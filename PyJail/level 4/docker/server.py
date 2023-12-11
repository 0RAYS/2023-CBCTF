WELCOME = '''
 _     _______     _______ _       _  _   
| |   | ____\ \   / / ____| |     | || |  
| |   |  _|  \ \ / /|  _| | |     | || |_ 
| |___| |___  \ V / | |___| |___  |__   _|
|_____|_____|  \_/  |_____|_____|    |_|  
                                          
'''

print(WELCOME)

print("Welcome to the JBNRZ's pyjail")
print("Enter your expression and I will evaluate it for you.")
print("Example: ")
print("  input: 1 + 1")
print("  Result: 2")
input_data = input("> ")
if len(input_data) > 12:
    print("It's too long to eval")
    exit(0)
try:
    print("Result: {}".format(eval(input_data)))
except Exception as e:
    print(f"Result: {e}")