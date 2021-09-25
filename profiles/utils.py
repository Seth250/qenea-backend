import random
from django.utils.crypto import get_random_string


def generate_random_username(prefix=None):
    min_length = 3
    max_length = 25
    add_prefix = False

    if prefix and len(prefix) in range(min_length, max_length):
        length = random.randrange(1, max_length - len(prefix))
        add_prefix = True
    else:
        length = random.randrange(min_length, max_length + 1)

    random_str = get_random_string(length=length)
    if add_prefix:
        return f'{prefix}_{random_str}'

    return random_str
    