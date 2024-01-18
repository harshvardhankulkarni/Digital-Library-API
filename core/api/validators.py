import re


def validate_email(email):
    if len(email) > 6:
        if re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) is not None:
            return True
    return False
