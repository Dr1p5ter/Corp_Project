import faker
import string
import random

LET = string.ascii_letters # all ascii letters
DIG = string.digits        # all ascii digits
SPE = "!@#$%^&*_+-=~"      # all special ascii letters

def gen_password(char_limit : int = 32) -> str :
    """ Generate random password of fixed length

    Builds password from available characters in header

    returns :
        randomized string of characters
    """
    return "".join([random.choice(LET + DIG + SPE) for i in range(char_limit)])

def gen_random_int(char_limit : int = 3) -> int :
    return "".join([random.choice(string.digits) for i in range(char_limit)])

def gen_username(firstname : str, lastname : str, char_limit : int = 32, minit : str = None, random_int_included : bool = 1) -> str :
    return str(firstname[0].lower() + (minit.lower() if minit != None else "") + lastname.lower() + (str(gen_random_int()) if random_int_included else ""))[0:char_limit]

def gen_name() -> list[str, str, str] :
    return (faker.Faker().unique.first_name(), random.choice(string.ascii_uppercase), faker.Faker().unique.last_name())

