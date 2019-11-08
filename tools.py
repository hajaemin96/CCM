from random import choice
import string

ABCDIG = string.ascii_letters + string.digits

def generate_short_name(length=8):
    return ''.join([choice(ABCDIG) for _ in range(length)])