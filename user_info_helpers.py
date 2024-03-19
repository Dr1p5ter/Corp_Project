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

    # place query inside cursor return the output
    Q = """
        SELECT *\nFROM user_info.login_credentials\nWHERE login_username = \"{0}\";
        """.format(username).strip()
    res = process_query(Q)
    return None if res == None else res[0]

def find_user_strike_count(user_id : str) -> int :
    """ Retrieve a user's strike count in permissions table

    Attempts to grab a user's strike count. This shouldn't fail but if it finds no user_id then
    the return will be None. Otherwise it will be an integer.

    returns :
        strike count as integer
        None if not found
    """

    # place query inside cursor return the output
    Q = """
        SELECT strike_count\nFROM user_info.permissions\nWHERE user_id = {0};
        """.format(user_id).strip()
    res = process_query(Q)
    return None if res == None else int(res[0][0])

def find_user_profile(user_id : str) -> list :
    """ Retrieve a user's profile tuple

    Attempts to grab the user's profile with regard to it's username

    returns :
        tuple consisting of (fname, minit, lname, b_date)
        None if not found
    """

    # place query inside cursor return the output
    Q = """
        SELECT fname, minit, lname, b_date\nFROM user_info.profile_info\nWHERE user_id = {0};
        """.format(user_id).strip()
    res = process_query(Q)
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

    # place query inside cursor return the output
    Q = """
        INSERT INTO user_info.login_credentials (login_username, login_password) VALUES (\"{0}\", \"{1}\");
        """.format(username, password).strip()
    return process_query(Q)

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

    # place query inside cursor return the output
    Q = """
        UPDATE user_info.login_credentials\nSET {0}{1} {2}\nWHERE login_username = \"{3}\";
        """.format("login_username = \"" + new_username + "\"" if (new_username != None) else "",
                   "," if ((new_username != None) and (new_password != None)) else "",
                   "login_password = \"" + new_password + "\"" if (new_password != None) else "",
                   old_username).strip()
    return process_query(Q)

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
    
    # make query variable
    Q = """
        DELETE FROM user_info.login_credentials\nWHERE user_id = {0}\nAND login_username = \"{1}\"\nAND login_password = \"{2}\";
        """.format(user_id, username, password).strip()
    return process_query(Q)

def update_user_permissions(user_id : str, new_strike_count : int) -> list :
    """ Change user's permissions based on strike count

    Attempts to modify the user's strike count. The trigger associated with the schema will manage
    all of the actual permission changes. If the strike count is the same for any reason nothing
    will changed.

    returns :
        list containing values related to the query commit on the cursor
    """
    # check if the new strike count is different
    if find_user_strike_count(user_id) == new_strike_count :
        logger.warning(colored("strike count is not different, nothing is modified in database", COL_WARNING))
        return None

    # place query inside cursor return the output
    Q = """
        UPDATE user_info.permissions\nSET strike_count = {0}\nWHERE user_id = {3};
        """.format(str(new_strike_count), user_id).strip()
    return process_query(Q)

def update_user_profile_info(user_id : str, new_fname : str = None, new_minit : str = None, new_lname : str = None, new_b_date : str = None) :
    """ Change user's profile based on provided details about that user

    Brute force attempt to update user profile. If any attribute is None they will be NULL in
    schema.

    returns :
        list containing values related to the query commit on the cursor    
    """
    # place query inside cursor return the output
    Q = """
        UPDATE user_info.profile_info\nSET fname = \"{0}\", minit = \"{1}\", lname = \"{2}\", b_date = \"{3}\"\nWHERE user_id = {4};
        """.format("NULL" if new_fname == None else new_fname,
                   "NULL" if new_minit == None else new_minit,
                   "NULL" if new_lname == None else new_lname,
                   "NULL" if new_b_date == None else new_b_date,
                   user_id).strip()
    return process_query(Q)
