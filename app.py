from flask import Flask, redirect, render_template, request

# Importar las funciones y algoritmo de cifrado/descifrado
import random
n = 0



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
    global n 
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


def encrypt(public_key, message):
    e, n = public_key
    
    encrypted_message = []
    for char in message:
        encrypted_char = pow(ord(char), e, n)
        encrypted_message.append(str(encrypted_char).zfill(4))
    return " ".join(encrypted_message)


def decrypt(private_key, ciphertext):
    d, n = private_key
    decrypted_message = ""
    ciphertext = ciphertext.split()
    for num in ciphertext:
        decrypted_char = pow(int(num), d, n)
        decrypted_message += chr(decrypted_char)
    return decrypted_message

# Crear la aplicación Flask
app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/encrypt')


# Definir la ruta para encriptar
@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt_message():
    global n   # Cambio de nombre de la función
    if request.method == 'POST':
        message = request.form['message']

        # Generar llaves
        public_key, private_key = generate_keypair()

        # Cifrar mensaje
        ciphertext = encrypt(public_key, message)
        n = public_key[1]


        return render_template('encrypt.html', message=message, ciphertext=ciphertext,
                               public_key=public_key, private_key=private_key)
    return render_template('encrypt.html')

# Definir la ruta para desencriptar
@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_message():
    global n
    print("Esto es n: ", str(n))
    if request.method == 'POST':
        ciphertext = request.form['ciphertext']
        private_key = (int(request.form['private_key']), n)  # Solo necesitamos el valor de d en la llave privada

        try:
            # Descifrar mensaje
            decrypted_message = decrypt(private_key, ciphertext)
        except ValueError:
            decrypted_message = "Error en la clave"  # Mensaje de error cuando la clave privada es incorrecta

        return render_template('decrypt.html', decrypted_message=decrypted_message)

    return render_template('decrypt.html')

# Resto del código omitido por brevedad

if __name__ == '__main__':
    app.run(debug=True)