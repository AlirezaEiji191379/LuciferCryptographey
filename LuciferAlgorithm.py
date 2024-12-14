sbox0_dict = {0: 12, 1: 15, 2: 7, 3: 10, 4: 14, 5: 13, 6: 11, 7: 0, 8: 2, 9: 6, 10: 3, 11: 1, 12: 9, 13: 4, 14: 5,
              15: 8}
sbox1_dict = {0: 7, 1: 2, 2: 14, 3: 9, 4: 3, 5: 11, 6: 0, 7: 4, 8: 12, 9: 13, 10: 1, 11: 10, 12: 6, 13: 15, 14: 8,
              15: 5}
permutation_table = {
    0: 10, 1: 21, 2: 52, 3: 56, 4: 27, 5: 1, 6: 47, 7: 38,
    8: 18, 9: 29, 10: 60, 11: 0, 12: 35, 13: 9, 14: 55, 15: 46,
    16: 26, 17: 37, 18: 4, 19: 8, 20: 43, 21: 17, 22: 63, 23: 54,
    24: 34, 25: 45, 26: 12, 27: 16, 28: 51, 29: 25, 30: 7, 31: 62,
    32: 42, 33: 53, 34: 20, 35: 24, 36: 59, 37: 33, 38: 15, 39: 6,
    40: 50, 41: 61, 42: 28, 43: 32, 44: 3, 45: 41, 46: 23, 47: 14,
    48: 58, 49: 5, 50: 36, 51: 40, 52: 11, 53: 49, 54: 31, 55: 22,
    56: 2, 57: 13, 58: 44, 59: 48, 60: 19, 61: 57, 62: 39, 63: 30
}


def GetSBoxZeroOutput(inputsBitsString):
    number = int(inputsBitsString, 2)
    return sbox0_dict[number]


def GetSBoxOneOutput(inputsBitsString):
    number = int(inputsBitsString, 2)
    return sbox1_dict[number]


def PermutateBits(inputBitsString):
    # inputBits are 64 bits!
    resultBitString = ""
    for i in range(0, 64):
        resultBitString = resultBitString + inputBitsString[permutation_table[i]]
    return resultBitString


