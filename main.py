from typing import List
import numpy as np
import random
import math

class Block_code:
    def __init__(self, c: List[int]) -> None:
        self.c = np.array(c)
        self.n = max(x.bit_length() for x in c)  # length of each codeword
        self.k = int(math.log2(len(c)))           # number of message bits
        self.d_min = min((weight(int(w)) for w in self.c if int(w) != 0), default=1)
        self.g = self.compute_generator_matrix()
        self.h = self.compute_paritycheck_matrix()
        self.syndrome_table = self.compute_syndrome_table()

    def compute_generator_matrix(self) -> np.ndarray:
        # find k linearly independent codewords then row-reduce them to systematic form.

        k, n = self.k, self.n

        # Convert each codeword integer to a length-n bit row (MSB first)
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
        #Derived from the systematic form of G = [I_k | P]:
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
 
        # Iterate over all 2^n possible error patterns
        for weight_limit in range(n + 1):
            for e in range(1 << n):
                if weight(e) != weight_limit:
                    continue
                s = tuple(self.syndrome(e))
                if s not in syndrome_table:
                    syndrome_table[s] = e
            # Early exit once all 2^(n-k) syndromes are accounted for
            if len(syndrome_table) == (1 << (n - self.k)):
                break
 
        return syndrome_table

    def send(self, message: int) -> int:
        k, n = self.k, self.n

        m_bits = np.array([(message >> (k - 1 - i)) & 1 for i in range(k)], dtype=int)
        codeword_bits = mod_two(np.matmul(m_bits, self.g))
        codeword = int("".join(map(str, codeword_bits)), 2)

        max_errors = self.d_min - 1

        if max_errors == 0:
            print(f"[send] codeword={bin(codeword)}, errors=0")
            return codeword

        num_errors = random.randint(0, max_errors)

        error_positions = random.sample(range(n), num_errors)
        error_pattern = sum(1 << (n - 1 - pos) for pos in error_positions)

        received = codeword ^ error_pattern

        print(f"[send] message={bin(message)}, codeword={bin(codeword)}, "
              f"errors={num_errors} at bits {error_positions}, received={bin(received)}")
        return received

    def decode(self, r: int) -> int:
        s = tuple(self.syndrome(r))
        zero_syndrome = tuple([0] * (self.n - self.k))

        if s == zero_syndrome:
            print(f"[decode] No errors detected. Received word={bin(r)} is a valid codeword.")
            return r
        else:
            error_pattern = self.syndrome_table[s]
            num_errors = weight(error_pattern)
            corrected = r ^ error_pattern

            print(f"[decode] {num_errors} error(s) detected and corrected. "
                  f"syndrome={s}, error_pattern={bin(error_pattern)}, "
                  f"corrected codeword={bin(corrected)}")
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

# TEST
b = Block_code([0, 22, 13, 27])

for msg in range(1 << b.k):
    received = b.send(msg)
    corrected = b.decode(received)
    assert corrected in b.c, f"Corrected word {bin(corrected)} not in codebook!"
