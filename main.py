from affine import Affine
from vigenere import Vigenere


def main():
    cipher_file = open('cipher.txt', 'r')
    cipher_text = cipher_file.read()
    print('*** cracking with affine cipher method ***')
    affine = Affine()
    decrypted = affine.crack(cipher_text)
    if decrypted:
        return decrypted
    print("*** can't crack with affine method ***")

    print("*** cracking with vigenere ***")
    vigenere = Vigenere()
    decrypted = vigenere.crack(cipher_text)
    if decrypted:
        return decrypted
    else:
        return None


if __name__ == '__main__':
    m = main()
    if m:
        print(f'cracked message is ====>\t {m}')
    else:
        print("Can't crack the message")
