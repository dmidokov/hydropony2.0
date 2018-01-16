
from __future__ import print_function
import mysql.connector as mysqli
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': 'ffuswgwy',
    'host': '127.0.0.1',
    'database':'hydropony'
}

cnx = mysqli.connect(**config)

cursor = cnx.cursor()
#data = (115,116,117,118)

add_dt = ("INSERT INTO hydrostats (temp,humidity,light,humidifier) VALUES ({},{},{},{})").format(90,91,93,92)

try: 
    cursor.execute(add_dt)
except mysqli.Error as err:
    print(err.msg)
else:
    print('OK')
cnx.commit()
cursor.close()
cnx.close()

