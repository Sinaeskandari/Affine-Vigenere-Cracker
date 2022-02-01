import enchant
import random


class Affine:
    def __init__(self):
        self.chars = {}  # adding all of letters from a to z with value of 0 to 25
        for i in range(ord('a'), ord('z') + 1):
            self.chars[chr(i)] = i - 97
        self.d = enchant.Dict('en_US')  # enchant dictionary for checking if a word is english or not

    def encrypt(self, plain, a, k):
        cipher = []
        for i in range(len(plain)):
            m = self.chars[plain[i]]
            cipher.append((a * m + k) % 26)
        cipher = [chr(j + 97) for j in cipher]
        return ''.join(cipher)

    def decrypt(self, cipher, a, k):
        a_inverse = pow(a, -1, 26)  # finding modular inverse of a, this method only works in python 3.8+
        plain = []
        for i in range(len(cipher)):
            m = self.chars[cipher[i]]
            plain.append((a_inverse * (m - k)) % 26)
        plain = [chr(j + 97) for j in plain]
        return ''.join(plain)

    def crack_word(self, cipher):
        # all key combinations
        k_list = [i for i in range(26)]
        a_list = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        possible_answers = []
        for a in a_list:
            for k in k_list:
                plain = self.decrypt(cipher, a, k)
                if self.d.check(plain):
                    possible_answers.append((a, k))
        return possible_answers

    def crack(self, cipher):
        cipher_list = cipher.split()
        # select a random word in cipher and find possible keys for it
        possible_answers = self.crack_word(random.choice(cipher_list))
        for i in possible_answers:
            plain_list = []
            a, k = i
            for word in cipher_list:
                plain_list.append(self.decrypt(word, a, k))
            # check if all the words are english
            is_english = [self.d.check(w) for w in plain_list]
            if all(is_english):
                return ' '.join(plain_list)


if __name__ == '__main__':
    c = Affine()
    ci = c.crack('qf qg y nkls ugfyxnqgruv tywf fryf y huyvuh cqnn xu vqgfhywfuv xa fru huyvyxnu wklfulf kt y jysu crul nkkoqls yf qfg nyakef')
    print(ci)
