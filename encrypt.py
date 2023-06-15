import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_keypair():
    p = random.randint(1000, 9999)
    q = random.randint(1000, 9999)

    while not (is_prime(p) and is_prime(q)):
        p = random.randint(1000, 9999)
        q = random.randint(1000, 9999)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    _, d, _ = extended_gcd(e, phi)
    d = d % phi
    if d < 0:
        d += phi

    return (e, n), (d, n)

def encrypt_rsa(public_key, message):
    e, n = public_key
    encrypted_message = []
    for char in message:
        encrypted_char = pow(ord(char), e, n)
        encrypted_message.append(str(encrypted_char).zfill(4))
    return " ".join(encrypted_message)

def decrypt_rsa(private_key, ciphertext):
    d, n = private_key
    decrypted_message = ""
    ciphertext = ciphertext.split()
    for num in ciphertext:
        decrypted_char = pow(int(num), d, n)
        decrypted_message += chr(decrypted_char)
    return decrypted_message

def encrypt_symmetric(message):
    encrypted_message = ""
    for char in message:
        encrypted_message += "miau"
    return encrypted_message

def decrypt_symmetric(ciphertext):
    decrypted_message = ""
    i = 0
    while i < len(ciphertext):
        decrypted_message += ciphertext[i:i+4]
        i += 4
    return decrypted_message

# Ejemplo de uso
public_key, private_key = generate_keypair()

message = "Hello"
ciphertext_rsa = encrypt_rsa(public_key, message)
ciphertext_symmetric = encrypt_symmetric(ciphertext_rsa)
decrypted_message_rsa = decrypt_rsa(private_key, ciphertext_rsa)
decrypted_message_symmetric = decrypt_symmetric(ciphertext_symmetric)

print("Mensaje original:", message)
print("Mensaje cifrado (RSA):", ciphertext_rsa)
print("Mensaje cifrado (simétrico):", ciphertext_symmetric)
print("Mensaje descifrado (RSA):", decrypted_message_rsa)
print("Mensaje descifrado (simétrico):", decrypted_message_symmetric)
