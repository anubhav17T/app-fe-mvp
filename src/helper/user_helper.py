import re
import random
import string


def check_user_metadata(data: dict):
    for key, value in data.keys():
        if value == "":
            return False


def check_password_strength(password):
    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    match = re.match(password_pattern, password)
    if match is None:
        return False
    return True


def check(email, password):
    if len(email) == 0:
        return False
    elif len(password) == 0:
        return False
    return True


def generate_random_word():
    letters_and_numbers = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_numbers) for _ in range(4))


# Generate 10 random words
