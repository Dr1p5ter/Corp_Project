import generator as gen

from user_info_helpers import *

if __name__ == "__main__" :
    user_dict = {}
    n_entries_to_gen = 25
    start_at_one = True
    user_id_begin_inc_at = 1

    for i in range(1 if start_at_one else 0, n_entries_to_gen + 1 if start_at_one else n_entries_to_gen) :
        f, m, l = gen.gen_name()
        username = gen.gen_username(f, l, minit = m, random_int_included = 1)
        password = gen.gen_password()
        key = "user_" + str(i)

        user_dict[key] = {
            "user_id" : user_id_begin_inc_at,
            "fname" : f,
            "minit" : m,
            "lname" : l,    
            "login_username" : username,
            "login_password" : password
        }
        user_id_begin_inc_at += 1

        try :
            res = insert_user_credentials(username, password)
            print(res) if res != None else ...
        except Exception as err :
            print(err)
            user_dict.pop(key)

    for key in user_dict.keys() :
        print(f'{key} -> {user_dict[key]}')

    for key in user_dict.keys() :
        res = delete_user_credentials(user_dict[key]["user_id"], user_dict[key]["login_username"], user_dict[key]["login_password"])
        print(res) if res != None else ...