import random
from io import StringIO
import sys

flag = open("/flag", "r").read()
BLACKED_LIST = ['compile', 'eval', 'exec', 'open']
eval_func = eval
for m in BLACKED_LIST:
    del __builtins__.__dict__[m]


def my_audit_hook(event, _):
    black = {'pty.spawn', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'subprocess.Popen'}
    if event in black:
        raise RuntimeError('Operation banned: {}'.format(event))


def guess():
    game_score = 0
    sys.stdout.write('Can u guess the number? between 1 and 1000 > ')
    sys.stdout.flush()
    my_lucky_num = [random.randint(1, 1000) for _ in range(5)]
    sys.stdout, sys.stderr, challenge_original_stdout = StringIO(), StringIO(), sys.stdout
    input_data = input()
    try:
        input_data = eval_func(input_data, {}, {})
    except:
        return game_score, my_lucky_num
    sys.stdout = challenge_original_stdout
    if input_data == my_lucky_num:
        game_score += 1
    return game_score, my_lucky_num


HELLO = '''
 _     _______     _______ _       _____ 
| |   | ____\ \   / / ____| |     |___  |
| |   |  _|  \ \ / /|  _| | |        / / 
| |___| |___  \ V / | |___| |___    / /  
|_____|_____|  \_/  |_____|_____|  /_/   
                                         
'''


def main():
    print(HELLO)
    choice = input('You have three choice:\n1. Play the guessing game\n2. Get important code about lucky_num\n> ')
    if choice == '1':
        print('Welcome to my game! \n\n,\nyou need to guess my five lucky numbers.\n\ninput_ex: [1, 2, 3, 4, 5]')
        score, nums = guess()
        if score == 1:
            print('Ohhh,you get it! Then I\'ll give you the secret key. Have a good time!')
            print(flag)
        else:
            print(f"The correct number is: {nums}")
            print('Please try again if you really want to play that game.')
    elif choice == '2':
        print("""
black = {'pty.spawn', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'subprocess.Popen'}

...        

def guess():
    game_score = 0
    sys.stdout.write('Can u guess the number? between 1 and 1000 > ')
    sys.stdout.flush()
    my_lucky_num = [random.randint(1, 1000) for _ in range(5)]
    sys.stdout, sys.stderr, challenge_original_stdout = StringIO(), StringIO(), sys.stdout
    input_data = input()
    try:
        input_data = eval_func(input_data, {}, {})
    except Exception:
        return game_score, my_lucky_num
    sys.stdout = challenge_original_stdout
    print(input_data)
    if input_data == my_lucky_num:
        game_score += 1
    return game_score, my_lucky_num""")
    else:
        print("What are you doing ???")


if __name__ == '__main__':
    sys.addaudithook(my_audit_hook)
    main()