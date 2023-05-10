# SQL - STRUCTURED QUERY LANGUAGE
# СУБД - Система Управления Базой Данных (SQLite)
# CRUD - Create, Reed, Update, Delete


import sqlite3

def create_connection(db_name):
    connection = sqlite3.connect(db_name)
    return connection


def create_table(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)


def create_student(conn, student: tuple):
    sql = '''INSERT INTO students 
    (full_name, mark, hobby, birth_date, is_married) VALUES 
    (?, ?, ?, ?, ?)'''
    cursor = conn.cursor()
    cursor.execute(sql, student)
    connection.commit()
# 1)

def select_all_students(conn):
    sql = '''SELECT * FROM students WHERE is_married;'''
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def delete_student(conn, id: int):
    sql = '''DELETE FROM students WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    connection.commit()


def update_student_mark(conn, id, mark):
    sql = '''UPDATE students SET mark = ? WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, (mark, id,))
    connection.commit()


sql_create_students_table = '''
CREATE TABLE IF NOT EXISTS students (
id INTEGER PRIMARY KEY AUTOINCREMENT, 
full_name VARCHAR (200) NOT NULL,
mark DOUBLE (5, 2) NOT NULL DEFAULT 0.0,
hobby TEXT DEFAULT NULL,
birth_date DATE NOT NULL,
is_married BOOLEAN DEFAULT FALSE
);
'''

connection = create_connection("school.db")


if connection:
    print("DB Connected!")

    create_table(connection, sql_create_students_table)
    select_all_students(connection)
    update_student_mark(connection, 2, 99)

    # delete_student(connection, 1)

    # create_student(connection, ("Esen", 50.21, None, "2003-06-08", False))

    # create_student(connection, ("Mark Daniels", 77.12, "Football", "1999-01-02", False))
    # create_student(connection, ("Alex Brilliant", 77.12, None, "1989-12-31", True))
    # create_student(connection, ("Diana Julls", 99.3, "Tennis", "2005-01-22", True))
    # create_student(connection, ("Michael Corse", 100.0, "Diving", "2001-09-17", True))
    # create_student(connection, ("Jack Moris", 50.2, "Fishing and cooking", "2001-07-12", True))
    # create_student(connection, ("Viola Manilson", 41.82, None, "1991-03-01", False))
    # create_student(connection, ("Joanna Moris", 100.0, "Painting and arts", "2004-04-13", False))
    # create_student(connection, ("Peter Parker", 32.0, "Travelling and bloging", "2002-11-28", False))
    # create_student(connection, ("Paula Parkerson", 77.09, None, "2001-11-28", True))
    # create_student(connection, ("George Newel", 93.0, "Photography", "1981-01-24", True))
    # create_student(connection, ("Miranda Alistoun", 87.55, "Playing computer games", "1997-12-22", False))
    # create_student(connection, ("Fiona Giordano", 66.12, "Driving fast", "1977-01-15", True))