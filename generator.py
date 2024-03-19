import faker
import string
import random

from datetime import datetime

from user_info_helpers import UILC_LU_MAX_LEN, UILC_LP_MAX_LEN

LET = string.ascii_letters # all ascii letters
DIG = string.digits        # all ascii digits
SPE = "!@#$%^&*_+-=~"      # all special ascii letters

year_limit = (1945, 2024)  # range of datetime year
month_limit = (1, 12)      # range of datetime month
day_limit = (1, 31)        # range of datetime day
hour_limit = (0, 23)       # range of datetime hour
minute_limit = (0, 59)     # range of datetime minute
second_limit = (0, 59)     # range of datetime second

def gen_password(char_limit : int = UILC_LP_MAX_LEN) -> str :
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

def gen_username(firstname : str, lastname : str, minit : str = None, char_limit : int = UILC_LU_MAX_LEN, random_int_included : bool = 1) -> str :
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
    return (faker.Faker().unique.first_name(), random.choice(LET).upper(), faker.Faker().unique.last_name())

def gen_datetime() -> datetime :
    """ Generate a fake datetime

    Construct a datetime that can be used for a fake bday date

    returns :
        datetime
    """
    yyyy = random.randrange(year_limit[0], year_limit[1] + 1)
    mm = random.randrange(month_limit[0], month_limit[1] + 1)
    dd = random.randrange(day_limit[0], day_limit[1] + 1)
    HH = random.randrange(hour_limit[0], hour_limit[1] + 1)
    MM = random.randrange(minute_limit[0], minute_limit[1] + 1)
    SS = random.randrange(second_limit[0], second_limit[1] + 1)
    return datetime(yyyy, mm, dd, HH, MM, SS)