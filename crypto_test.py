from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# 256-bit kalit yaratish
key = AESGCM.generate_key(bit_length=256)

aesgcm = AESGCM(key)

# boshlang'ich qiymat (nonce)
nonce = os.urandom(12)

data = b"Secret message"

# shifrlash
ciphertext = aesgcm.encrypt(nonce, data, None)

print("Shifrlangan ma'lumot:")
print(ciphertext)

# deshifrlash
plaintext = aesgcm.decrypt(nonce, ciphertext, None)

print("Deshifrlangan ma'lumot:")
print(plaintext)