from sql_helpers import *
from termcolor import *

UILC_LU_MAX_LEN = 16 # user_info.login_credentials.login_username max length
UILC_LP_MAX_LEN = 32 # user_info.login_credentials.login_password max length

def find_user_info(username : str) -> list :
    # generate cursor and grab connection pointer
    con, cur = generate_connction_cursor()

    # place query inside cursor
    cur.execute(
        """
        SELECT user_id, login_username, login_password 
        FROM user_info.login_credentials AS lc
        WHERE lc.login_username = "{0}";
        """.format(username)
    )

    # return and close
    return get_and_close(con, cur)

def insert_user_credentials(username : str, password : str) -> list :
    # generate cursor and grab connection pointer
    con, cur = generate_connction_cursor()

    # place query inside cursor
    try :
        cur.execute(
            """
            INSERT INTO user_info.login_credentials (login_username, login_password)
            VALUES ("{0}", "{1}");
            """.format(username, password)
        )
    except mysql.connector.IntegrityError as err :
        print(err)
        get_and_close(con, cur)
        return None
    except Exception as err :
        print(err)
        get_and_close(con, cur)
        return None
    
    # return and close
    return get_and_close(con, cur)

def update_user_credentials(old_username : str, new_username : str = None, new_password : str = None) -> list :
    # figure out if the user_id exists
    if find_user_info(old_username) == None :
        print(colored("old username was not found in database", COL_WARNING))
        return None
    
    # check if any argument is not None
    if (new_username is None) and (new_password is None) :
        print(colored("no new username or passsword was provided", COL_WARNING))
        return None

    # generate cursor and grab connection pointer
    con, cur = generate_connction_cursor()

    # place query inside cursor
    Q = """
        UPDATE user_info.login_credentials\nSET {0}{1} {2}\nWHERE login_username = \"{3}\"
        """.format("login_username = \"" + new_username + "\"" if (new_username != None) else "",
                   "," if ((new_username != None) and (new_password != None)) else "",
                   "login_password = \"" + new_password + "\"" if (new_password != None) else "",
                   old_username).strip()
    try :
        print(colored("Query to process :", COL_HEADER))
        print(colored(Q, COL_CONTEXT))
        cur.execute(Q)
    except Exception as err :
        print(colored(err, COL_ERROR))
        get_and_close(con, cur)
        return None

    # return and close
    print(colored("update was successful", COL_SUCCESS))
    return get_and_close(con, cur)