import generator as gen

from sql_helpers import *
from user_info_helpers import *

if __name__ == "__main__" :

    # TODO: fill in window here in future

    ...

    # user_dict = dict()
    # n_entries_to_gen = 50
    # start_at_one = True
    # user_id_begin_inc_at = 1

    # for i in range(1 if start_at_one else 0, n_entries_to_gen + 1 if start_at_one else n_entries_to_gen) :
    #     f, m, l = gen.gen_name()
    #     username = gen.gen_username(f, l, minit = m, random_int_included = (int(random.choice(string.digits)) % 2))
    #     password = gen.gen_password()

    #     user_dict[i] = {
    #         "user_id" : user_id_begin_inc_at,
    #         "fname" : f,
    #         "minit" : m,
    #         "lname" : l,
    #         "login_username" : username,
    #         "login_password" : password
    #     }
    #     user_id_begin_inc_at += 1

    #     try :
    #         print(insert_user_credentials(username, password))
    #     except Exception :
    #         user_dict.pop(i)

    # print(update_user_credentials("new_me", new_username = "bad_user", new_password = "bad_pass"))
    # print(update_user_credentials(user_dict[0]["login_username"], new_username = "new_user", new_password = "new_pass"))
    # print(update_user_credentials(user_dict[1]["login_username"], new_password = "new_pass"))
    # print(update_user_credentials(user_dict[2]["login_username"], new_username = "new_user"))
    # print(update_user_credentials(user_dict[3]["login_username"]))
