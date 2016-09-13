import os
import sys

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """create a db connection using the supplied database file
    :param db_file: database to connect to 
    :return: Codjlfnection to db or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print e 
    return None

def close_connection(conn):
    """closes connection
        :param conn: Connection object
    """
    conn.close()


def commit(conn):
    """commits the transactions on the db
    :param conn: connection object
    """
    conn.commit()

def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print e

def insert_into(conn, table_name, columns, values):
    """  Inserts provided values into specified table + columns
        :param conn: Connection Object
        :param table_name: Name of table to insert values into
        :param columns: Array or string of column names
        :param values: Tuple containing values to be inserted
    """
    try:
        values_string = "?"
        if isinstance(columns, basestring):
           #sanitizing input to be an array if string
           columns = columns.split(',') 
        for i in range(len(columns)-1):
            values_string = values_string + "," + values_string
        
        columns = ','.join(columns) #making sure columns is formatted correctly
        INSERT_STRING = (
            "INSERT INTO {0} ( {1} ) "
            "VALUES({2})"
        ).format(table_name, columns, values_string)
        c = conn.cursor()
        c.execute(INSERT_STRING, values)
    except Error as e:
        print e

def select_all_from(conn, table_name):
    """ selects all entries from the given table on the given database
        :param conn: Connection Object
        :param table_name: table to select from as a string
        :return: selected values
    """
    sql = (
        "SELECT * FROM {}").format(table_name)
    c = conn.cursor()
    c.execute(sql) 
    return c.fetchall()
    
    
