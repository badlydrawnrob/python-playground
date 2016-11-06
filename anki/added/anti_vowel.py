'''
Anti vowel | Practice makes perfect.8

'''


def anti_vowel(text):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    string = ''

    for c in text:
        if c.lower() in vowels:
            continue
        else:
            string += c

    return string


print(anti_vowel('Hello'))
