from collections import deque

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
    return format(sbox0_dict[number], '04b')


def GetSBoxOneOutput(inputsBitsString):
    number = int(inputsBitsString, 2)
    return format(sbox1_dict[number], '04b')


def PermutateBits(inputBitsString):
    # inputBits are 64 bits!
    resultBitString = ""
    for i in range(0, 64):
        resultBitString = resultBitString + inputBitsString[permutation_table[i]]
    return resultBitString


def xor_binary_strings(bin_str1, bin_str2):
    max_len = max(len(bin_str1), len(bin_str2))
    bin_str1 = bin_str1.zfill(max_len)
    bin_str2 = bin_str2.zfill(max_len)
    int1 = int(bin_str1, 2)
    int2 = int(bin_str2, 2)
    xor_result = int1 ^ int2
    return format(xor_result, f'0{max_len}b')


def GetFiestelInnerFunctionOutput(rightBranch, subKey):
    sboxes_control_bits = subKey[56:]
    resultBitString = ""
    for i in range(0, 8):
        control_bit = sboxes_control_bits[i]
        byte_index = i * 8
        sbox_input_byte = rightBranch[byte_index: byte_index + 8]
        left_nibble = sbox_input_byte[:4]
        right_nibble = sbox_input_byte[4:]
        if control_bit == "0":
            resultBitString = resultBitString + GetSBoxZeroOutput(right_nibble) + GetSBoxOneOutput(left_nibble)
        else:
            resultBitString = resultBitString + GetSBoxZeroOutput(left_nibble) + GetSBoxOneOutput(right_nibble)
    resultBitString = xor_binary_strings(resultBitString, subKey)
    resultBitString = PermutateBits(resultBitString)
    return resultBitString


def rotate_left(s, n):
    d = deque(s)
    d.rotate(-n)
    return ''.join(d)


def KeySchedule(keyBitsString):
    subKeys = []
    subKeys.append(keyBitsString[:64])
    for i in range(1, 16):
        keyBitsString = rotate_left(keyBitsString, 56)
        subKeys.append(keyBitsString[:64])
    return subKeys


def string_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_string(binary_str):
    chars = [binary_str[i:i + 8] for i in range(0, len(binary_str), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)


x = ['0011000100110010001100110011010000110101001101100011011100111000',
     '0011100000111001001100000011000100110010001100110011010000110101',
     '0011010100110110001100010011001000110011001101000011010100110110',
     '0011011000110111001110000011100100110000001100010011001000110011',
     '0011001100110100001101010011011000110001001100100011001100110100',
     '0011010000110101001101100011011100111000001110010011000000110001',
     '0011000100110010001100110011010000110101001101100011000100110010',
     '0011001000110011001101000011010100110110001101110011100000111001',
     '0011100100110000001100010011001000110011001101000011010100110110',
     '0011011000110001001100100011001100110100001101010011011000110111',
     '0011011100111000001110010011000000110001001100100011001100110100',
     '0011010000110101001101100011000100110010001100110011010000110101',
     '0011010100110110001101110011100000111001001100000011000100110010',
     '0011001000110011001101000011010100110110001100010011001000110011',
     '0011001100110100001101010011011000110111001110000011100100110000',
     '0011000000110001001100100011001100110100001101010011011000110001']

def EncryptData(plainText, key, is_enc):
    input_str = string_to_binary(plainText)
    key = string_to_binary(key)
    subKeys = KeySchedule(key)
    if not is_enc:
        subKeys.reverse()
    Ls = []
    Rs = []
    L = input_str[0:64]
    R = input_str[64:]
    Ls.append(L)
    Rs.append(R)
    for i in range(0, 16):
        f = xor_binary_strings(GetFiestelInnerFunctionOutput(R, subKeys[i]), L)
        L = R
        R = f
        Ls.append(L)
        Rs.append(R)
    return binary_to_string(L + R), Ls, Rs


cipher, Ls, Rs = EncryptData("rezaeijirezaeiji", "1234567890123456", True)
print(cipher)
LL = ['0111001001100101011110100110000101100101011010010110101001101001', '0011000100110010001100110011010000110101001101100011011100111000', '0111101101101110011110010110010001100010011011000110100101100100', '0011110000111101001100100011011100110100001100010011011000111011', '0111100001101111011100000110111101100001011010010110111001100001', '0011100100111110001111110011100000110101001100100011011100111100', '0111111101101110011100110110111001101000011000100110110101100100', '0011110000111001001110100011101100111000001111010011011000111111', '0111110001101111011101000110111101101011011000110110010001101111', '0011011100111010001111110011110000111101001111100011101100110000', '0111001101101110011101110110111001101100011000100110011101101110', '0011011000110011001101000011111100111000001110010011111000110011', '0111000001100011011110000110111101101111011000110110000001101111', '0011011100110000001101010011011000110011001110100011101100110100', '0111011101100110011110110110001001100000011000100110001101101110', '0011011000110111001101000011010100110010001100110011000000110111', '0111001001100101011110100110000101100101011010010110101001101001']
RR = ['0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111001001100101011110100110000101100101011010010110101001101001', '0111010001100011011111000110011101100011011011110110110001101111']

for i in range(0, 16):
    print("#########")
    print(Rs[i])
    print(RR[i])
    if RR[i] == Rs[i]:
        print(i)


