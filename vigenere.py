import itertools
import enchant


class Vigenere:
    def __init__(self):
        self.chars = {}  # adding all of letters from a to z with value of 0 to 25
        for i in range(ord('a'), ord('z') + 1):
            self.chars[chr(i)] = i - 97
        self.d = enchant.Dict('en_US')  # enchant dictionary for checking if a word is english or not
        # frequency of english letters
        self.english_letter_freq = {'e': 13, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7, 'n': 6.7, 's': 6.3,
                                    'h': 6.1, 'r': 6, 'd': 4.3, 'l': 4, 'c': 2.8, 'u': 2.8, 'm': 2.4,
                                    'w': 2.4, 'f': 2.2, 'g': 2, 'y': 2, 'p': 1.9, 'b': 1.5, 'v': 0.98,
                                    'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07}
        self.letters_sorted = 'etaoinshrdlcumwfgypbvkjxqz'  # english letters sorted
        self.cipher_with_spaces = ''  # used later to add spaces between cracked message

    def decrypt(self, cipher, key):
        # generate key with appropriate length
        rep = len(cipher) // len(key)
        excess = len(cipher) % len(key)
        extended_key = key * rep + key[:excess]
        plain = ''
        for i in range(len(extended_key)):
            k = (self.chars[cipher[i]] - self.chars[extended_key[i]]) % 26
            plain += chr(k + 97)
        return plain

    def get_factors(self, n):
        # get all factors of a number between 2 and 16
        return [i for i in range(2, 17) if n % i == 0]

    def find_repeated(self, message):
        # find sub words with size of 2 to 5 that is repeated through cipher text
        sub_word_distance = {}
        for i in range(2, 6):
            for s in range(len(message) - i):
                seq = message[s:s + i]
                for j in range(s + i, len(message) - i):
                    if message[j:j + i] == seq:
                        if seq not in sub_word_distance:
                            sub_word_distance[seq] = []
                        sub_word_distance[seq].append(j - s)
        return sub_word_distance

    def get_possible_key_lengths(self, sub_word_distance):
        # count the factors
        factors_count = {}
        for key in sub_word_distance:
            for i in sub_word_distance[key]:
                for j in self.get_factors(i):
                    if j not in factors_count:
                        factors_count[j] = 0
                    factors_count[j] += 1
        # sort the factors descending to get all possible key length in order of most occurrences
        possible_key_lengths = [k for k, v in sorted(factors_count.items(), key=lambda a: a[1], reverse=True)]
        return possible_key_lengths

    def get_sub_letters(self, key_length, message):
        # get a list of letters that are encrypted by the same key
        sub_letters = []
        for i in range(key_length):
            sub_letters.append(''.join([message[j] for j in range(len(message)) if j % key_length == i]))
        return sub_letters

    def frequency_count(self, message):
        # assign a frequency to each decrypted message
        # count number of occurrences of each letter
        letter_count_dict = {i: 0 for i in self.chars.keys()}
        for j in message:
            letter_count_dict[j] += 1
        # sort letter counts to compare to most used and least used english letters
        letter_freq_sorted = ''.join(
            [i for i, j in sorted(letter_count_dict.items(), key=lambda item: item[1], reverse=True)])
        freq = 0
        # add to freq if a letter in first 6 letters of the sorted message letter is also in first 6 most used english letters
        for l in self.letters_sorted[:6]:
            if l in letter_freq_sorted[:6]:
                freq += 1
        # add to freq if a letter in last 6 letters of the sorted message letter is also in 6 least used english letters
        for l in self.letters_sorted[-6:]:
            if l in letter_freq_sorted[-6:]:
                freq += 1
        return freq

    def add_spacing(self, message):
        s = 0
        message_list = []
        # add appropriate spacing based on the spacing in cipher text
        for i in self.cipher_with_spaces.split():
            e = len(i) + s
            message_list.append(message[s:e])
            s = e
        return message_list

    def is_english(self, message):
        # check if decrypted message is english
        message_list = self.add_spacing(message)
        is_english_list = [self.d.check(i) for i in message_list]
        return all(is_english_list)

    def crack_with_key_len(self, cipher, key_length):
        sub_letters = self.get_sub_letters(key_length, cipher)
        # calculate frequency of all nth sub letters and use them to get all possible option for each key spot
        frequency_count = []
        for sub_letter in sub_letters:
            sub_letter_frequency_count = [(l, self.frequency_count((self.decrypt(sub_letter, l)))) for l in
                                          self.chars.keys()]
            sub_letter_frequency_count.sort(key=lambda a: a[1], reverse=True)
            frequency_count.append(sub_letter_frequency_count[:4])  # only use top 4
        combination_letters = []
        for i in frequency_count:
            comb = []
            for j in i:
                comb.append(j[0])
            combination_letters.append(comb)
        # generate all possible keys with the combinations calculated
        for possible_key in itertools.product(*combination_letters):
            possible_key = ''.join(possible_key)
            decrypted = self.decrypt(cipher, possible_key)
            if self.is_english(decrypted):
                return decrypted

    def crack(self, cipher):
        cipher = cipher.lower()
        self.cipher_with_spaces = cipher  # save spacing of message for later
        cipher = cipher.replace(' ', '')  # remove spaces for decryption
        possible_key_lengths = self.get_possible_key_lengths(self.find_repeated(cipher))
        for key_length in possible_key_lengths:
            plain = self.crack_with_key_len(cipher, key_length)
            if plain:
                return ' '.join(self.add_spacing(plain))


if __name__ == '__main__':
    v = Vigenere()
    a = 'alp amalzy wttwpalrelhpsy afvztosz e dph vj mlgpg zasyeetcuw ez kvvv hwal dfpzxteiamzy qptspfz'
    print(v.crack(a))
