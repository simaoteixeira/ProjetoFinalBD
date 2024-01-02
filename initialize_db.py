# this script is used to initialize the database
"""
    1. if the database exists, make a backup of the database and drop the database
    2. Create a new database
    3. Create tables
    4. Create all database objects
    5. Insert data into tables
    6. Create different users:
        - admin
        - compras
        - vendas
        - stock
        - producao
    7. Add privileges to users:
        - admin has all privileges
        - compras has objects related to purchases
        - vendas has objects related to sales
        - stock has objects related to stock
        - producao has objects related to production
"""
import os
import sys
from datetime import datetime
from pathlib import Path
import psycopg2

# SET CONSTANTS read .env file from ./ProjetoFinal/.env
import environ

env = environ.Env()
environ.Env.read_env('./ProjetoFinal/.env')

# SET CONSTANTS
DB_HOST = env('DB_HOST')
DB_NAME = env('DB_NAME')
DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')
DB_PORT = env("DB_PORT")

BASE_DIR = Path(__file__).resolve().parent.parent

BACKUP_DIR = './backups'

# CREATE BACKUP DIRECTORY
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)


def main():
    # connect to default database
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
    except psycopg2.OperationalError as e:
        print(f'Error connecting to database: {e}')
        sys.exit(1)

    # create cursor
    cur = conn.cursor()
    conn.autocommit = True

    # check if database exists
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")

    # if database exists, make a backup of the database
    if cur.fetchone():
        # create backup file
        backup_file = f'{BACKUP_DIR}/{DB_NAME}-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'

        # create backup command
        """
            database: DB_NAME
            host: DB_HOST
            port: DB_PORT
            username: DB_USER
            password: DB_PASSWORD
            
            custom format: directory
            file_name: backup_file
            do not save: owner privileges, tablespace assignments 
            dump data and schema of objects
            
                    
            -Fc: custom format
            -f: file name
            -d: database name
            -h: host
            -p: port
            -U: username
            -W: password
            -v: verbose
            -O: no owner privileges
            -x: do not save tablespace assignments
            -b: dump data and schema of objects
        """

        backup_command = f'pg_dump --dbname=postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME} -Fd -j 5 -f {backup_file}  -v -O -x -b'
        print(f'Creating backup: {backup_command}')
        # execute backup command
        response = os.system(backup_command)

        if response != 0:
            print(f'Error creating backup: {response}')
            sys.exit(1)

        print(f'Backup created: {backup_file}')

    # drop all connections to database
    cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
                f"FROM pg_stat_activity "
                f"WHERE datname = '{DB_NAME}' "
                f"AND leader_pid IS NULL;")

    # drop database if exists
    cur.execute(f'DROP DATABASE IF EXISTS {DB_NAME};')

    # create database
    cur.execute(f'CREATE DATABASE {DB_NAME};')

    # close connection to default database
    cur.close()
    conn.close()

    # connect to new database
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
    except psycopg2.OperationalError as e:
        print(f'Error connecting to database: {e}')
        sys.exit(1)

    # execute manage.py migrate to create all django tables
    os.system('python manage.py migrate')

    # create cursor
    cur = conn.cursor()
    conn.autocommit = True

    print('Creating tables...')

    # create tables
    cur.execute(open('./ScriptsBD/bd_create.sql', 'r').read())

    print('Tables created')

    print('Creating database objects...')

    # create database objects
    cur.execute(open('./ScriptsBD/Procedures&Functions&Views.sql', 'r').read())

    print('Database objects created')

    print('Inserting data into tables...')

    os.system(f'python manage.py shell < create_django_users.py')

    # insert data into tables
    cur.execute(open('./ScriptsBD/inserts.sql', 'r').read())

    print('Data inserted')

    print('Creating users and granting privilieges...')

    # create users
    cur.execute(open('./ScriptsBD/create_users.sql', 'r').read())

    print('Users created')

    # close cursor
    cur.close()

    # close connection to database
    conn.close()


if __name__ == '__main__':
    main()
