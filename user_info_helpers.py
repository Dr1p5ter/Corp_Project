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
        tuple consisting of (user_id, login_username, login_password, last_password_change, need_password_change)
        None if not found
    """
    # generate cursor and grab connection pointer
    con, cur = generate_connction_cursor()

    # place query inside cursor return the output
    Q = """
        SELECT *\nFROM user_info.login_credentials\nWHERE login_username = \"{0}\";
        """.format(username).strip()
    res = process_query(Q, con, cur)
    return None if res == None else res[0]

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

    # place query inside cursor return the output
    Q = """
        INSERT INTO user_info.login_credentials (login_username, login_password) VALUES (\"{0}\", \"{1}\");
        """.format(username, password).strip()
    return process_query(Q, con, cur)

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
        logger.warning(colored("old username \'{0}\' was not found in database : nothing updated".format(old_username), COL_WARNING))
        return None

    # check if any argument is not None
    if (new_username is None) and (new_password is None) :
        logger.warning(colored("no new username or passsword was provided : nothing updated", COL_WARNING))
        return None

    # generate cursor and grab connection pointer
    con, cur = generate_connction_cursor()

    # place query inside cursor return the output
    Q = """
        UPDATE user_info.login_credentials\nSET {0}{1} {2}\nWHERE login_username = \"{3}\"
        """.format("login_username = \"" + new_username + "\"" if (new_username != None) else "",
                   "," if ((new_username != None) and (new_password != None)) else "",
                   "login_password = \"" + new_password + "\"" if (new_password != None) else "",
                   old_username).strip()
    return process_query(Q, con, cur)

def delete_user_credentials(user_id : int, username : str, password : str) -> list :
    """ Deletes user from user_credentials

    Brute force approach for removal of user_id from the records inside of user_credentials. This
    requires no checking with the hardship of confirming record.

    returns :
        list containing values related to the query commit on the cursor
    """
    
    # validate inputs before proceeding
    if find_user_info(username) == None :
        logger.warning(colored("username \'{0}\' was not found in database : nothing deleted".format(username), COL_WARNING))
        return None
    
    # proceed with deletion of record
    # generate cursor and grab connection pointer
    con, cur = generate_connction_cursor()

    # make query variable
    Q = """
        DELETE FROM user_info.login_credentials\nWHERE user_id = {0}\nAND login_username = \"{1}\"\nAND login_password = \"{2}\";
        """.format(user_id, username, password).strip()
    return process_query(Q, con, cur)