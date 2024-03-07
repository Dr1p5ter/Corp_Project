import mysql.connector

from logger import logger
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from sys import exit
from termcolor import colored

HOST = "localhost"                                     # host name to the server
ADMIN_CRED_USER = "admin_console"                      # username for the admin terminal
ADMIN_CRED_PASS = "8l>R$fTe`j!6V9QvWgG<5#.KTLl4:<'P"   # password for the admin terminal

COL_HEADER = "blue"                                    # color constants for printing in
COL_CONTEXT = "magenta"                                # other helper modules
COL_SUCCESS = "green"                                  #
COL_WARNING = "yellow"                                 #
COL_ERROR = "red"                                      #

def generate_connction_cursor() -> list[MySQLConnection, MySQLCursor] :
    """ Start connection to MySQL server

    This function will create both a connector and cursor. The function returns None if
    for whatever reason the connection or cursor couldn't be made given admin credentials. Else
    the function will return cursor and connection tuple.

    returns :
        con -> pointer to connector object
        cur -> pointer to the connector opjects cursor object
    """

    try :
        # log into MySQL server
        con = mysql.connector.connect(
            host = HOST,
            user = ADMIN_CRED_USER,
            password = ADMIN_CRED_PASS
        )

        # create a buffered cursor
        cur = con.cursor(buffered=True)
    except Exception as err :
        logger.error(colored(err, COL_ERROR))
        return None

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

    try :
        # commit the query made using cursor
        con.commit()
    except Exception as err :
        logger.error(colored(err, COL_ERROR))

    # fetch all lines from the commit
    try :
        fetch = cur.fetchall()
    except :
        fetch = None

    # close the cursor and connection
    if not cur.close() :
        logger.error(colored("Cursor was not able to be disconnected or bad cursor", COL_ERROR))
        return None
        
    if not con.close() :
        logger.error(colored("Connection was not able to be closed or bad connection", COL_ERROR))
        return None

    # return all the lines from the query
    return None if (fetch == []) else fetch

def process_query(query : str, con : MySQLConnection, cur : MySQLCursor) -> list :
    """ Abstraction to process queries for other helper modules

    Executes the query and closes the connection while returning the output.

    returns :
        list containing values related to the query commit on the cursor
    """
    try :
        # pass the query into the cursor
        logger.info(colored("Query to process :", COL_HEADER) + '\n' + colored(query, COL_CONTEXT))
        cur.execute(query)
    except Exception as err :
        # log error if execution fails for any reason
        logger.error(colored(err, COL_ERROR))
        get_and_close(con, cur)
        return None

    # return and close
    logger.info(colored("select was successful", COL_SUCCESS))
    return get_and_close(con, cur)