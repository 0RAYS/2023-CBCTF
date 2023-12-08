import struct

def mem2bin(mem : list[int]) -> bytes:
    
    return b''.join([struct.pack('<I', x) for x in mem])

def bin2mem(bin : bytes) -> list[int]:
    size = len(bin)
    if (size % 4) != 0:
        size = ((size + 3) // 4) * 4
        bin = bin.ljust(size, b'\0')
    
    result = []
    for i in range(0, size, 4):
        block = bin[i:i+4]
        result.append(struct.unpack('<I', block)[0])
    return result

if __name__ == "__main__":
    a = mem2bin([2, 3, 4])
    print(a)
    b = bin2mem(a)
    print(b)