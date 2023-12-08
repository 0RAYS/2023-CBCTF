

def gen_putstr_tight(s : str, number=0):
    header = '_STR%d:\n' % number
    header2 = '_PUT%d:\n' % number
    pattern1 = 'raw #%x\n'
    pattern2 = 'put [%%_STR' + ('%d' % number) + '+%x]\n'
    result = [header]
    result2 = [header2]
    for i, ch in enumerate(s):
        n = ord(ch)
        result.append(pattern1 % n)
        result2.append(pattern2 % i)
    
    return ''.join(result + result2)

def gen_putstr(s : str, number=0):
    header = '_PUT%d:\n' % number
    pattern = 'put #%x\n'
    result = [header]
    for ch in s:
        n = ord(ch)
        result.append(pattern % n)
    
    return ''.join(result)

if __name__ == "__main__":
    s = "Welcome to CBCTF 2023!\nNow guess my lucky number:"

    res = gen_putstr_tight(s)
    print(res)