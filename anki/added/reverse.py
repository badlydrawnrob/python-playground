'''
Reverse | Practice Makes Perfect.7

'''


def reverse(text):
    current = 0
    reverse = []

    for c in text:
        reverse.insert(current, c)
        current = reverse.index(c)

    return ''.join(reverse)


print(reverse('this@2!'))


def reverse_slowly(text):
    reversed_text = ''
    slicing = len(text) - 1  # 'hello' = [0:3]

    # For each letter in text
    # - text_length, minus current character

    for i in range(len(text)):
        reversed_text += text[slicing - i]
    return reversed_text


print(reverse_slowly('this@2!'))


def reverse_even_slower(text):
    new_text = []
    index = len(text)

    while index:
        index -= 1
        new_text.append(text[index])
    return ''.join(new_text)


print(reverse_even_slower('this@2!'))
