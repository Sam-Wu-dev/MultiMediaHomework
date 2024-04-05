

def gf_multiply(x, y):
    """Multiply two numbers in GF(2^8)."""
    r = 0
    for i in range(8):
        if (y & 1) == 1:
            r ^= x
        hbit = x & 0x80
        x <<= 1
        if hbit == 0x80:
            x ^= 0x1b # Reduction polynomial x^8 + x^4 + x^3 + x + 1
        y >>= 1
    return r & 0xFF

x = gf_multiply(0x11,0x31)
print(f'{x:02x}')