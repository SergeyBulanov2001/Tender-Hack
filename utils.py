import random
import string


def generate_token(length):
    alphabet = string.ascii_letters
    token = ''
    for i in range(length):
        token += alphabet[random.randint(0, len(alphabet) - 1)]
    return token
