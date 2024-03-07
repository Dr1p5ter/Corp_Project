from sql_helpers import *

UILC_LU_MAX_LEN = 16 # user_info.login_credentials.login_username max length
UILC_LP_MAX_LEN = 32 # user_info.login_credentials.login_password max length

def is_username_valid(username : str) -> bool :
    """ Validate username
    
    Check if the username is unique and is within length

    returns :
        True if valid, False otherwise
    """
    if find_user_info(username) != None :
        logger.error(colored("username already exists within database", COL_ERROR))
        return False
    if len(username) > UILC_LU_MAX_LEN :
        logger.error(colored("username length must not exceed {0} characters".format(UILC_LU_MAX_LEN), COL_ERROR))
        return False
    return True

def is_password_valid(password : str) -> bool :
    """ Validate password

    Check if the password is within length

    returns :
        True if valid, Flase otherwise
    """
    if len(password) > UILC_LP_MAX_LEN :
        logger.error(colored("password length must not exceed {0} characters".format(UILC_LP_MAX_LEN), COL_ERROR))
        return False
    return True

def find_user_info(username : str) -> list :
    """ Retrieve a user's information tuple

    Attempts to grab the user's information with regard to it's username

    returns :
        tuple of users id, username, and password
        None if not found
    """
    # generate cursor and grab connection pointer
    con, cur = generate_connction_cursor()

    # place query inside cursor
    Q = """
        SELECT user_id, login_username, login_password\nFROM user_info.login_credentials\nWHERE login_username = "{0}";
        """.format(username).strip()
    logger.info(colored("Query to process :", COL_HEADER) + '\n' + colored(Q, COL_CONTEXT))
    cur.execute(Q)

    # return and close
    logger.info(colored("select was successful", COL_SUCCESS))
    return get_and_close(con, cur)

def insert_user_credentials(username : str, password : str) -> list :
    """ Insert a users credentials into the database
    
    Given a users username and password, insert them into the database.

    returns :
        list containing values related to the query commit on the cursor
    """
    # validate inputs before proceeding
    if (not is_username_valid(username)) or (not is_password_valid(password)) :
        logger.warning(colored("username or password not valid/violates schema : {nothing inserted}", COL_WARNING))
        return None

    # generate cursor and grab connection pointer
    con, cur = generate_connction_cursor()

    # place query inside cursor
    Q = """
        INSERT INTO user_info.login_credentials (login_username, login_password) VALUES (\"{0}\", \"{1}\");
        """.format(username, password).strip()
    try :
        # pass the query into the cursor
        logger.info(colored("Query to process :", COL_HEADER) + '\n' + colored(Q, COL_CONTEXT))
        cur.execute(Q)
    except Exception as err :
        logger.error(colored(err, COL_ERROR))
        get_and_close(con, cur)
        return None
    
    # return and close
    logger.info(colored("select was successful", COL_SUCCESS))
    return get_and_close(con, cur)

def update_user_credentials(old_username : str, new_username : str = None, new_password : str = None) -> list :
    """ Attempt to update user credentials

    Change the username or password of a user who is already in the database.
    This attempts to check the old username to see if it exists, and if there is an input for a
    new username or password. If those two are satisfied then update the credentials.

    returns :
        list containing values related to the query commit on the cursor
    """

    # figure out if the user_id exists
    if find_user_info(old_username) == None :
        logger.warning(colored("old username \'{0}\' was not found in database : {nothing updated}".format(old_username), COL_WARNING))
        return None

    # check if any argument is not None
    if (new_username is None) and (new_password is None) :
        logger.warning(colored("no new username or passsword was provided : {nothing updated}", COL_WARNING))
        return None

    # generate cursor and grab connection pointer
    con, cur = generate_connction_cursor()

    # make query variable
    Q = """
        UPDATE user_info.login_credentials\nSET {0}{1} {2}\nWHERE login_username = \"{3}\"
        """.format("login_username = \"" + new_username + "\"" if (new_username != None) else "",
                   "," if ((new_username != None) and (new_password != None)) else "",
                   "login_password = \"" + new_password + "\"" if (new_password != None) else "",
                   old_username).strip()
    try :
        # pass the query into the cursor
        logger.info(colored("Query to process :", COL_HEADER) + '\n' + colored(Q, COL_CONTEXT))
        cur.execute(Q)
    except Exception as err :
        # log error if execution fails for any reason
        logger.error(colored(err, COL_ERROR))
        get_and_close(con, cur)
        return None

    # return and close
    logger.info(colored("select was successful", COL_SUCCESS))
    return get_and_close(con, cur)