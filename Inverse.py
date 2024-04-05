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

def gf_inverse(x):
    """Compute multiplicative inverse in GF(2^8) using Extended Euclidean Algorithm."""
    if x == 0:
        return 0
    u = x
    v = 0x11b # Reduction polynomial x^8 + x^4 + x^3 + x + 1
    g1 = 1
    g2 = 0
    while u != 1:
        j = len(bin(u)) - len(bin(v))
        if j < 0:
            u, v = v, u
            g1, g2 = g2, g1
            j = -j
        u = u ^ (v << j)
        g1 = g1 ^ (g2 << j)
    return g1

def gf_add(x, y):
    """Add two numbers in GF(2^8). Addition is XOR in GF(2^8)."""
    return x ^ y

def gf_matrix_multiply(A, B, n=4):
    """Multiply two matrices in GF(2^8)."""
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cell = 0
            for k in range(n):
                cell ^= gf_multiply(A[i][k], B[k][j])
            result[i][j] = cell
    return result

def gf_matrix_inverse(A, n=4):
    """Invert an nxn matrix in GF(2^8)."""
    # Append identity matrix to A to start the process
    temp = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(A)]
    
    for i in range(n):
        # Make diagonal element 1 by multiplying the row by its inverse
        inv = gf_inverse(temp[i][i])
        for j in range(n*2):  # Corrected from 8 to n*2
            temp[i][j] = gf_multiply(temp[i][j], inv)
        
        # Make all other elements in current column 0
        for k in range(n):
            if k != i:
                factor = temp[k][i]
                for j in range(n*2):  # Corrected from 8 to n*2
                    temp[k][j] ^= gf_multiply(factor, temp[i][j])
    
    # Extract the inverse matrix from the modified temp
    return [row[n:] for row in temp]

# Use the matrix A as defined in the previous cell.
# Compute the inverse

# Example 4x4 matrix in GF(2^8)
A = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

# Compute the inverse
A_inv = gf_matrix_inverse(A)

print("A:")
for row in A:
    print(' '.join([f'{val:02x}' for val in row]))
    
print("A^-1:")
for row in A_inv:
    print(' '.join([f'{val:02x}' for val in row]))
    
print("A * A^-1:")

I = gf_matrix_multiply(A,A_inv)

for row in I:
    print(' '.join([f'{val:02x}' for val in row]))
