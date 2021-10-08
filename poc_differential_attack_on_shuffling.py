"""
This is a simplified proof-of-concept of the differential algebraic attack
applied to dummyless shuffling.

The setting is simulated by shuffling the 16 first round S-box outputs
of the AES and mixing linearly with a few more random bits (128).

Tested on:
┌────────────────────────────────────────────────────────────────────┐
│ SageMath version 9.4, Release Date: 2021-08-22                     │
│ Using Python 3.9.5. Type "help()" for help.                        │
└────────────────────────────────────────────────────────────────────┘
"""

from sage.all import *


def int_to_bits(v, n):
    return tuple(ZZ(v).digits(2, padto=n)[::-1])


# AES S-box
S = (99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22)

key = [int(randrange(256)) for _ in range(16)]
print("generated secret key:", key)

# random linear mixing matrix
PAD = 16
while True:
    n = (16 + PAD)*8
    MIX = random_matrix(GF(2), n, n)
    if MIX.is_invertible():
        break


def trace(pt):
    res = [S[b ^ k] for b, k in zip(pt, key)]
    shuffle(res)
    res += [randrange(256) for _ in range(PAD)]

    bits = ()
    for v in res:
        bits += int_to_bits(v, 8)
    return MIX * vector(GF(2), bits)


recovered_key = [None] * 16
n_traces = 0
for pos in range(16):
    print("attacking position", pos)
    rows = []
    pts = []
    pts2 = []
    n = (16 + PAD)*8 + 50

    print("collecting", n, "pairs")
    for _ in range(n):
        pt = [int(randrange(256)) for _ in range(16)]
        diff = randrange(1, 256)
        pt2 = pt[::]
        pt2[pos] ^= diff
        pts.append(pt)
        pts2.append(pt2)

        t1 = trace(pt)
        t2 = trace(pt2)
        diff = t1 + t2  # XOR the two traces
        rows.append(diff)
        n_traces += 2

    # homework: how to reduce n^3*256 to n^3 + n^2*256 ?

    print("attacking")
    mat = matrix(rows)
    for k in range(256):
        # compute guessed sensitive function
        target = []
        for row, pt, pt2 in zip(rows, pts, pts2):
            out = S[pt[pos] ^ k] ^ S[pt2[pos] ^ k]
            target.append(int_to_bits(out, 8)[0])
        target = vector(GF(2), target)

        # check guessed sensitive function
        try:
            mat.solve_right(target)
            print("pos", pos, "key byte", k, "matches")
            recovered_key[pos] = k
        except:
            continue

print("recovered key", "".join("%02x" % c for c in recovered_key))
print("   actual key", "".join("%02x" % c for c in key))
print(" total traces", n_traces)
