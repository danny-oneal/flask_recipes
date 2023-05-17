import re


def is_length(str, max, min=0):
    return len(str) >= min and (max == None or len(str) <= max)


def is_email(str):
    # https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    reg_ex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
    return reg_ex.match(str)


def is_present(str):
    return len(str) > 0


def is_password(str):
    # https://stackoverflow.com/questions/19605150/regex-for-password-must-contain-at-least-eight-characters-at-least-one-number-a
    reg_ex = re.compile(
        r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    )
    return is_length(str, min=8, max=72) and reg_ex.match(str)


def is_match(str1, str2):
    return str1 == str2
