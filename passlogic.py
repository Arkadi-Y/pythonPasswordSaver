import binascii
import sqlite3
import os
import cryptography
from cryptography.fernet import Fernet


# sql connection
def setUpSql():
    connection = sqlite3.connect('Pass.db')
    cursor = connection.cursor()
    # first time run
    try:
        cursor.execute('''CREATE TABLE passwords
                     (programName text, ID text, password text, encrypted BIT)''')
    # table already created
    except sqlite3.Error:
        connection.close()
    finally:
        # close connection
        if connection:
            connection.close()


# name says it all
def checkDuplicate(app, mail, data):
    for row in data:
        if app in row and mail in row:
            return True


# enter data to sql
def WriteData(name, Id, password, key, encrypted):
    # connect
    connection = sqlite3.connect('Pass.db')
    cursor = connection.cursor()
    sqlite3_Insert = """INSERT INTO passwords
                              (programName, ID, password,encrypted) 
                              VALUES (?, ?, ?,?);"""
    # set values
    if encrypted:
        data_tuple = (name, Id, encrypt(password, key), 1)
    else:
        data_tuple = (name, Id, password, 0)
    # commit
    cursor.execute(sqlite3_Insert, data_tuple)
    connection.commit()
    # close
    cursor.close()
    connection.close()


# update data in sql
def updateData(name, Id, password, key, encrypted, lastApp, lastID):
    # connect
    connection = sqlite3.connect('Pass.db')
    cursor = connection.cursor()
    sqlite3_Insert = """UPDATE passwords
                            SET 
                              programName = ?,
                              ID = ?,
                              password= ?,
                              encrypted = ?
                            WHERE
                                 programName = ? AND ID = ?
                              ;"""
    # set values
    if encrypted:
        data_tuple = (name, Id, encrypt(password, key), 1, lastApp, lastID)
    else:
        data_tuple = (name, Id, password, 0, lastApp, lastID)
    # commit
    cursor.execute(sqlite3_Insert, data_tuple)
    connection.commit()
    # close
    cursor.close()
    connection.close()


def DeleteRow(appName, ID):
    # connect
    connection = sqlite3.connect('Pass.db')
    cursor = connection.cursor()
    data_tuple = (appName, ID)
    sqlite3_Insert = """DELETE FROM passwords
                                  WHERE  programName =? AND ID=?;"""
    # commit
    cursor.execute(sqlite3_Insert, data_tuple)
    connection.commit()
    # close
    cursor.close()
    connection.close()


# read from sql
def ReadData(key):
    # connect
    connection = sqlite3.connect('Pass.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM passwords")
    Data = cursor.fetchall()
    # to array
    data = [list(i) for i in Data]
    cursor.close()
    # loop array to decrypt password
    for rowNum, rowData in enumerate(data):
        rowData = list(rowData)
        # check if password encrypted
        if data[rowNum][3] == 1:
            try:
                data[rowNum][2] = decrypt(rowData[2], key).decode("utf-8")
                # catch wrong keys
            except AttributeError:
                data[rowNum][2] = "Key doesnt match"
    # close
    if connection:
        connection.close()
    # return array with decrypted passwords
    return data


# import key from file directory
def setKey(Dir):
    try:
        with open(Dir, 'a+') as myKeyFile:
            # check if file is empty
            if os.stat(Dir).st_size == 0:
                print("file empty")
                # create new key
                newKey = Fernet.generate_key()
                print(newKey)
                myKeyFile.write(newKey.decode('utf-8'))
                key = newKey.decode('utf-8')
            else:
                # read file
                myKeyFile.seek(0)
                key = myKeyFile.read()
            return key
    except FileNotFoundError:
        # will never get here because of handling in dir select at pyqtUI
        return "key file not found"


def encrypt(password, Key):
    password = password.encode('utf_8')
    try:
        return Fernet(Key).encrypt(password)
    except cryptography.fernet.InvalidToken:
        return 'cryptography.fernet.InvalidToken'
    except binascii.Error:
        return 'binascii.Error'
    except ValueError:
        return 'ValueError'


def decrypt(password, Key):
    try:
        return Fernet(Key).decrypt(password)
    except cryptography.fernet.InvalidToken:
        print("Wrong key - will show 'Key doesnt match' at 91")
    except binascii.Error:
        return 'binascii.Error'
    except TypeError:
        return 'TypeError'
    except ValueError:
        return 'ValueError'
