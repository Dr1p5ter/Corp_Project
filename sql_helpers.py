import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from logger import *

HOST = "localhost"                                     # host name to the server
ADMIN_CRED_USER = "admin_console"                      # username for the admin terminal
ADMIN_CRED_PASS = "8l>R$fTe`j!6V9QvWgG<5#.KTLl4:<'P"   # password for the admin terminal

COL_HEADER = "blue"                                    # color constants for printing in
COL_CONTEXT = "magenta"                             # other helper modules
COL_SUCCESS = "green"                                  #
COL_WARNING = "yellow"                                 #
COL_ERROR = "red"                                      #

def generate_connction_cursor() -> list[MySQLConnection, MySQLCursor] :
    """ Start connection to MySQL server

    This function will create both a connector and cursor.

    returns :
        con -> pointer to connector object
        cur -> pointer to the connector opjects cursor object
    """

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
    """ Fetch all lines from cursor and close connection
    
    Attempts to grab all lines returned by the cursors execution once commited, iff there is
    lines to grab from the cursors output. Once done, it will close the cursor then the
    connection.

    returns :
        fetch -> an array of strings associated with each line of the cursors output
    """

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
    return None if (fetch == []) else fetch
