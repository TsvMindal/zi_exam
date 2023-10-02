import subprocess

#Напишите программу, реализующую процедуру MixColomns шифра AES
#(длина блока равна 128 битов). Входные и выходные данные должны быть представлены в виде квадрата.

def generate_random_hex_string(length):
    result = subprocess.run(["openssl", "rand", "-hex", str(length)], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def gf_multiply(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        if a & 0x80:
            a = (a << 1) ^ 0x1b
        else:
            a <<= 1
        b >>= 1
    return result

def mix_columns(matrix):
    mixed_columns_result = [[0] * 4 for _ in range(4)]

    for column in range(4):
        mixed_columns_result[0][column] = gf_multiply(0x02, matrix[0][column]) ^ gf_multiply(0x03, matrix[1][column]) ^ matrix[2][column] ^ matrix[3][column]
        mixed_columns_result[1][column] = matrix[0][column] ^ gf_multiply(0x02, matrix[1][column]) ^ gf_multiply(0x03, matrix[2][column]) ^ matrix[3][column]
        mixed_columns_result[2][column] = matrix[0][column] ^ matrix[1][column] ^ gf_multiply(0x02, matrix[2][column]) ^ gf_multiply(0x03, matrix[3][column])
        mixed_columns_result[3][column] = gf_multiply(0x03, matrix[0][column]) ^ matrix[1][column] ^ matrix[2][column] ^ gf_multiply(0x02, matrix[3][column])

    return mixed_columns_result

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f'{x:02x}' for x in row))
    print()


hex_data = generate_random_hex_string(16)

raw_data = [int(hex_data[i:i+2], 16) for i in range(0, 32, 2)]

matrix = [raw_data[i:i+4] for i in range(0, 16, 4)]

print("Исходная матрица:")
print_matrix(matrix)

mix_columns_matrix = mix_columns(matrix)

print("Матрица MixColumns:")
print_matrix(mix_columns_matrix)


