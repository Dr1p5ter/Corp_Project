import faker
import string
import random

def gen_password(char_limit : int = 16) -> str :
    return "".join([random.choice(string.ascii_letters + string.digits + "!@#$%^&*_+-=~") for i in range(len)])

def gen_random_int(len : int = 3) -> int :
    return "".join([random.choice(string.digits) for i in range(len)])

def gen_username(firstname : str, lastname : str, char_limit : int, minit : str = None, random_int_included : bool = 1) -> str :
    return str(firstname[0].lower() + (minit.lower() if minit != None else "") + lastname.lower() + (str(gen_random_int()) if random_int_included else ""))[0:char_limit]

def gen_name() -> list[str, str, str] :
    return (faker.Faker().unique.first_name(), random.choice(string.ascii_uppercase), faker.Faker().unique.last_name())

