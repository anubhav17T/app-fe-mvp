import re


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