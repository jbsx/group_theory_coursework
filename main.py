from typing import List
from itertools import combinations
import numpy as np
import random
import math

class Block_code:
    def __init__(self, c: List[int]) -> None:
        self.c = np.array(c)
        self.n = max(x.bit_length() for x in c)
        self.k = int(math.log2(len(c)))
        self.d_min = min((weight(int(w)) for w in self.c if int(w) != 0), default=1)
        self.max_detectable = self.d_min - 1
        self.max_correctable = (self.d_min - 1) // 2
        self.g = self.compute_generator_matrix()
        self.h = self.compute_paritycheck_matrix()
        self.syndrome_table = self.compute_syndrome_table()

    def compute_generator_matrix(self) -> np.ndarray:
        # find k linearly independent codewords then row-reduce them to systematic form.

        k, n = self.k, self.n

        # Convert each codeword integer to a length-n bit row
        rows = []
        for word in self.c:
            row = [(int(word) >> (n - 1 - i)) & 1 for i in range(n)]
            rows.append(row)

        # Gaussian elimination in Z_2
        matrix = np.array(rows, dtype=int)
        basis = []
        pivot_cols = []
        row_idx = 0

        for col in range(n):
            # Find a pivot in this column at or below row_idx
            found = -1
            for r in range(row_idx, len(matrix)):
                if matrix[r, col] == 1:
                    found = r
                    break
            if found == -1:
                continue

            # Swap pivot row into position
            matrix[[row_idx, found]] = matrix[[found, row_idx]]

            # Eliminate all other 1s in this column
            for r in range(len(matrix)):
                if r != row_idx and matrix[r, col] == 1:
                    matrix[r] = (matrix[r] + matrix[row_idx]) % 2

            basis.append(matrix[row_idx].copy())
            pivot_cols.append(col)
            row_idx += 1

            if len(basis) == k:
                break

        return np.array(basis, dtype=int)  # shape: (k, n)

    def compute_paritycheck_matrix(self) -> np.ndarray:
        # Derived from the systematic form of G = [I_k | P]:
        #    H = [P^T | I_(n-k)]

        k, n = self.k, self.n
        r = n - k

        G = self.g  # shape (k, n)

        # Identify pivot columns (one per row of G)
        pivot_cols = []
        for row in range(k):
            for col in range(n):
                if G[row, col] == 1 and col not in pivot_cols:
                    pivot_cols.append(col)
                    break

        parity_cols = [c for c in range(n) if c not in pivot_cols]

        # P is the k×r submatrix of G at the parity columns
        P = G[:, parity_cols]  # shape (k, r)
        PT = P.T               # shape (r, k)

        # Build H with correct column placement
        H = np.zeros((r, n), dtype=int)

        # Place P^T under the pivot columns
        for j, pc in enumerate(pivot_cols):
            H[:, pc] = PT[:, j]   # j-th column of P^T -> pivot column pc

        # Place I_r under the parity columns
        for i, pc in enumerate(parity_cols):
            H[i, pc] = 1

        return H  # shape: (n-k, n)

    def syndrome(self, x: int):
        # Returns HC_t
        c = [(x >> (self.n - 1 - i)) & 1 for i in range(self.n)]
        return mod_two(np.matmul(self.h, np.array(c).transpose()))

    def compute_syndrome_table(self):
        n = self.n
        syndrome_table = {}
        syndrome_table[tuple(self.syndrome(0))] = 0

        for weight_limit in range(1, n + 1):
            for positions in combinations(range(n), weight_limit):
                e = sum(1 << (n - 1 - p) for p in positions)
                s = tuple(self.syndrome(e))
                if s not in syndrome_table:
                    syndrome_table[s] = e

            if len(syndrome_table) == (1 << (n - self.k)):
                break

        return syndrome_table

    def encode(self, message: int) -> int:
        m_bits = np.array([(message >> (self.k - 1 - i)) & 1 for i in range(self.k)], dtype=int)
        codeword_bits = mod_two(np.matmul(m_bits, self.g)) # C = m \dot G
        codeword = int("".join(map(str, codeword_bits)), 2)
        return codeword

    def decode(self, codeword: int) -> int:
        pivot_cols = []
        for row in range(self.k):
            for col in range(self.n):
                if self.g[row, col] == 1 and col not in pivot_cols:
                    # Ensure this column is an identity column (only 1 in this row)
                    if all(self.g[r, col] == 0 for r in range(self.k) if r != row):
                        pivot_cols.append(col)
                        break

        codeword_bits = [(codeword >> (self.n - 1 - i)) & 1 for i in range(self.n)]
        msg_bits = [codeword_bits[i] for i in pivot_cols]
        return int("".join(map(str, msg_bits)), 2)

    def correct(self, r: int) -> int:
        s = tuple(self.syndrome(r))

        zero_syndrome = tuple([0] * (self.n - self.k))
        if s == zero_syndrome:
            return r


        if s not in self.syndrome_table:
            raise ValueError(f"Invalid input")

        # weight of valid coset leader must be <= correctable weight
        error_pattern = self.syndrome_table[s]
        if weight(self.syndrome_table[s]) > self.max_correctable:
            raise ValueError(f"Too many errors detected. Errors:{weight(error_pattern)}")

        corrected = r ^ error_pattern
        return corrected

# Helper Functions
def weight(x: int) -> int:
    length = 0
    while x:
        if x & 1:
            length += 1
        x = x >> 1
    return length

def mod_two(w: np.ndarray):
    for idx in range(len(w)):
        w[idx] %= 2
    return w

def send(codeword: int, n: int, errors: int) -> int:
    if errors == 0:
        return codeword

    #Generate random error pattern -> XOR with codeword
    error_positions = random.sample(range(n), errors)
    error_pattern = sum(1 << (n - 1 - pos) for pos in error_positions)
    received = codeword ^ error_pattern
    return received

def binary(x: int) -> List[int]:
    return [int(x >> (4 - 1 - i)) & 1 for i in range(4)]

# TEST
b = Block_code([0, 22, 13, 27])

for _ in range(1000):
    for msg in range(1 << b.k):
        codeword = b.encode(msg)
        received = send(codeword, b.n, random.randint(0, b.max_detectable - 1))
        corrected = b.correct(received)
        decoded = b.decode(corrected)
        assert msg == decoded
        #if msg != decoded:
        #    print(f" Message: {binary(msg)},\n Codeword:{binary(codeword)},\n Received:{binary(received)},\n Corrected: {binary(corrected)},\n Decoded: {binary(decoded)}\n")
