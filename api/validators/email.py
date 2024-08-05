import re
class EmailValidator:
    @staticmethod
    def validate(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False
        else:
            return True