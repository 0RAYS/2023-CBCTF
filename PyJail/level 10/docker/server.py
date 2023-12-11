import load_flag


def main():
    WELCOME = '''
 _     _______     _______ _       _  ___  
| |   | ____\ \   / / ____| |     / |/ _ \ 
| |   |  _|  \ \ / /|  _| | |     | | | | |
| |___| |___  \ V / | |___| |___  | | |_| |
|_____|_____|  \_/  |_____|_____| |_|\___/ 
                                           
'''
    print(WELCOME)
    print("It's so easy challenge!")
    print("Seems flag into the dir()")
    repl()


def repl():
    my_global_dict = dict()
    my_global_dict['flag'] = load_flag.get_flag()
    input_code = input("> ")
    complie_code = compile(input_code, '<string>', 'single')
    exec(complie_code, my_global_dict)


if __name__ == '__main__':
    main()