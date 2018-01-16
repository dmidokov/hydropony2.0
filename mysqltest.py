from __future__ import print_function
import mysql.connector as mysqli
from mysql.connector import errorcode
def create_database(cursor):
        try:
            cursor.execute(
           "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysqli.Error as err:
           print("Failed creating database: {}".format(err))
           exit(1)
        try:
            cnx.database = DB_NAME  
        except mysqli.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                cnx.database = DB_NAME
            else:
                print(err)
                exit(1)

DB_NAME = 'hydroponytest'

TABLES = {}
TABLES['employees'] = (
        "CREATE TABLE employees ("
        " emp_no int(11) NOT NULL AUTO_INCREMENT,"
        " birth_date date NOT NULL,"
        " first_name varchar(14) NOT NULL,"
        " last_name varchar(16) NOT NULL,"
        " gender enum('M','F') NOT NULL,"
        " hire_date date  NOT NULL, "
        " PRIMARY KEY (emp_no) "
        " ) ENGINE innoDB")
TABLES['departments']= (
        "CREATE TABLE departments ("
        " dept_no char(4) NOT NULL,"
         "  dept_name varchar(40) NOT NULL,"
        " PRIMARY KEY (dept_no), UNIQUE KEY dept_name (dept_name)"
        " ) ENGINE innoDB")

TABLES['salaries'] = (
        "CREATE TABLE salaries ("
        "  emp_no int(11) NOT NULL,"
       "  salary int(11) NOT NULL,"
       "  from_date date NOT NULL,"
       "  to_date date NOT NULL,"
       "  PRIMARY KEY (emp_no,from_date), KEY emp_no (emp_no),"
       "  CONSTRAINT salaries_ibfk_1 FOREIGN KEY (emp_no) "
       "     REFERENCES employees (emp_no) ON DELETE CASCADE"
       ") ENGINE=InnoDB")

TABLES['deptemp'] = (
       "CREATE TABLE deptemp ("
       "  emp_no int(11) NOT NULL,"
       "  dept_no char(4) NOT NULL,"
       "  from_date date NOT NULL,"
       "  to_date date NOT NULL,"
       "  PRIMARY KEY (emp_no,dept_no), KEY emp_no (emp_no),"
       "  KEY dept_no (dept_no),"
       "  CONSTRAINT dept_emp_ibfk_1 FOREIGN KEY (emp_no) "
       "     REFERENCES employees (emp_no) ON DELETE CASCADE,"
       "  CONSTRAINT dept_emp_ibfk_2 FOREIGN KEY (dept_no) "
       "     REFERENCES departments (dept_no) ON DELETE CASCADE"
       ") ENGINE=InnoDB")

TABLES['deptmanager'] = (
       "  CREATE TABLE deptmanager ("
       "  dept_no char(4) NOT NULL,"
       "  emp_no int(11) NOT NULL,"
       "  from_date date NOT NULL,"
       "  to_date date NOT NULL,"
       "  PRIMARY KEY (emp_no,dept_no),"
       "  KEY emp_no (emp_no),"
       "  KEY dept_no (dept_no),"
       "  CONSTRAINT dept_manager_ibfk_1 FOREIGN KEY (emp_no) "
       "     REFERENCES employees (emp_no) ON DELETE CASCADE,"
       "  CONSTRAINT dept_manager_ibfk_2 FOREIGN KEY (dept_no) "
       "     REFERENCES departments (dept_no) ON DELETE CASCADE"
       ") ENGINE=InnoDB")

TABLES['titles'] = (
       "CREATE TABLE titles ("
       "  emp_no int(11) NOT NULL,"
       "  title varchar(50) NOT NULL,"
       "  from_date date NOT NULL,"
       "  to_date date DEFAULT NULL,"
       "  PRIMARY KEY (emp_no,title,from_date), KEY emp_no (emp_no),"
       "  CONSTRAINT titles_ibfk_1 FOREIGN KEY (emp_no)"
       "     REFERENCES employees (emp_no) ON DELETE CASCADE"
       ") ENGINE=InnoDB")

config = {
       'user': 'root',
       'password': 'ffuswgwy',
       'host': '127.0.0.1',
       'database':'hydroponytest'
       }

cnx = mysqli.connect(**config)

cursor = cnx.cursor()
#create_database(cursor)
#cnx.database = 'hydropony'
for name,dd1 in TABLES.items():
    try:
        print("Creating table {}: ".format(name),end="")
        cursor.execute(dd1)
    except mysqli.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print('OK')


cursor.close()
cnx.close()





