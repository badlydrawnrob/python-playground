'''
Censor! | Practice makes perfect.10

'''


def censor(text, word):
        text = text.split()  # Convert to list
        word_length = len(word)  # For our ****

        for i, item in enumerate(text):
            if item == word:
                asterix = '*' * word_length
                text[i] = asterix
                print("{} yup! '{}' is the same as '{}'".format(i, item, word))
                print('Replacing {} with {}'.format(i, asterix))
            else:
                print('{} is not {}'.format(i, word))

        return ' '.join(text)


print(censor('this is a sentence', 'sentence'))
