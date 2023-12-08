buf = []
def getchar():
    global buf
    while len(buf) <= 0:
        buf = list(input().encode())
        buf.append(0x0a)
    return buf.pop(0)

def run():
    mem = eval(open('checkin.tricode', 'r').read())
    ip = 0
    size = len(mem)
    while ip + 2 < size:
        a1 = mem[ip]
        a2 = mem[ip + 1]
        a3 = mem[ip + 2]
        next_jump = ip + 3

        if a2 & 0x80000000 != 0:
            print(chr(mem[a1]), end='')
        elif a1 & 0x80000000 != 0:
            mem[a2] = getchar()
        else:
            mem[a2] = (mem[a2] - mem[a1]) & 0xffffffff
            if mem[a2] == 0 or mem[a2] & 0x80000000 != 0:
                next_jump = a3

        ip = next_jump
    
if __name__ == "__main__":
    run()