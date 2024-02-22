import mysql.connector
import generator as gen
import random
import string

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

HOST = "localhost"
ADMIN_CRED_USER = "admin_console"
ADMIN_CRED_PASS = "8l>R$fTe`j!6V9QvWgG<5#.KTLl4:<'P"

def generate_connction_cursor() -> list[MySQLConnection, MySQLCursor] :
    # log into MySQL server
    con = mysql.connector.connect(
        host = HOST,
        user = ADMIN_CRED_USER,
        password = ADMIN_CRED_PASS
    )

    # create a buffered cursor
    cur = con.cursor(buffered=True)

    # return pointers to connector and cursor
    return (con, cur)

def get_and_close(con : MySQLConnection, cur : MySQLCursor) -> list :
    # commit the query made using cursor
    con.commit()

    # fetch all lines from the commit
    try :
        fetch = cur.fetchall()
    except :
        fetch = None

    # close the cursor and connection
    cur.close()
    con.close()

    # return all the lines from the query
    return fetch

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
        return None
    
    # check if any argument is not None
    if (new_username is None) and (new_password is None) :
        return None

    # generate cursor and grab connection pointer
    con, cur = generate_connction_cursor()

    # place query inside cursor
    try :
        cur.execute(
            """
            UPDATE user_info.login_credentials
            {0}
            {1}
            WHERE login_username = {2}
            """.format("login_username = " + new_username + ", " if (new_username != None) else "",
                       "login_password = " + new_password + ", " if (new_password != None) else "",
                       old_username)
        )
    except Exception as err :
        print(err)
        get_and_close(con, cur)
        return None

    # return and close
    return get_and_close(con, cur)

if __name__ == "__main__" :

    for i in range(50) :
        f, m, l = gen.gen_name()
        username = gen.gen_username(f, l, 16, minit = m, random_int_included = (int(random.choice(string.digits)) % 2))
        password = gen.gen_password(32)
        print(insert_user_credentials(username, password))