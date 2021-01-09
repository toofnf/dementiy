import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    ciphertext = ""
    s = [x for x in plaintext]
    for i in range(len(s)):
        if (64 < ord(s[i]) < 91 - shift) or (96 < ord(s[i]) < 123 - shift):
            s[i] = chr(ord(s[i]) + shift)
        elif 90 - shift < ord(s[i]) < 91:
            s[i] = chr(shift - 26 + ord(s[i]))
        elif 122 - shift < ord(s[i]) < 123:
            s[i] = chr(shift - 26 + ord(s[i]))
    return ciphertext.join(s)


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    c = [x for x in ciphertext]
    for i in range(len(c)):
        if (64 + shift < ord(c[i]) < 91) or (96 + shift < ord(c[i]) < 123):
            c[i] = chr(ord(c[i]) - shift)
        elif 64 < ord(c[i]) < 65 + shift:
            c[i] = chr(26 - shift + ord(c[i]))
        elif 96 < ord(ciphertext[i]) < 97 + shift:
            c[i] = chr(26 - shift + ord(c[i]))
    return plaintext.join(c)

def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
