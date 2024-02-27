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
    """ Generate random int suffix for username generation

    Builds string of random digits within char limit

    returns :
        randomized integer string of digits
    """
    return "".join([random.choice(DIG) for i in range(char_limit)])

def gen_username(firstname : str, lastname : str, char_limit : int = 32, minit : str = None, random_int_included : bool = 1) -> str :
    """ Generate username of fixed length

    Construct a username given a set name

    returns :
        uniformly generated username
    """
    return str(firstname[0].lower() + (minit.lower() if minit != None else "") + lastname.lower() + (str(gen_random_int()) if random_int_included else ""))[0:char_limit]

def gen_name() -> list[str, str, str] :
    """ Generate fake name

    Construct a fake name used for account generation for testing

    returns :
        tuple of first name, middle initial, and last name
    """
    return (faker.Faker().unique.first_name(), random.choice(LET), faker.Faker().unique.last_name())
