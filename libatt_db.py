# ===== PROBLEMA =====
# Hindi na-track ng library kung sino ang regular na pumupunta, kung ano libro ang hihiramin,
# kung anong PC ang ginagamit ng mga estudyante, at hindi rin nila alam kung sino ang
# pinaka-active na bumibisita sa library para sa rewards.
#
# ===== SOLUSYON =====
# Library Attendance & Usage System na nagre-record ng pagpasok/paglabas ng estudyante,
# nagtatanong kung gagamit ba ng PC o may hihiramin bang libro, nag-a-assign ng available na PC,
# nagtatala kung sino ang gumagamit ng aling PC, nagbibigay ng points kada bisita,
# at may leaderboard para makita ang pinaka-marami ang punta sa library para sa reward.

import os

import mysql.connector
from mysql.connector import Error


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "library_attendance_db")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        use_pure=True,
    )


def test_connection():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM students LIMIT 1")
            cursor.fetchone()
            return True, "Koneksyon sa Library Attendance & Usage database ay OK na."
        return False, "Hindi makakonekta sa database."
    except Error as error:
        return False, str(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# STUDENTS
def add_student(student_id, full_name, grade_level, section):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (student_id, full_name, grade_level, section) VALUES (%s,%s,%s,%s)",
            (student_id, full_name, grade_level, section),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def find_student(student_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def update_student_points_visits(student_id, points_add):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET total_visits = total_visits + 1, total_points = total_points + %s WHERE student_id = %s",
            (points_add, student_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# BOOKS
def add_book(book_id, title, author):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO books (book_id, title, author, available) VALUES (%s,%s,%s,1)",
            (book_id, title, author),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def list_books():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books ORDER BY title")
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def find_book(book_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def borrow_book(book_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE books SET available = 0 WHERE book_id = %s AND available = 1", (book_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def return_book(book_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE books SET available = 1 WHERE book_id = %s", (book_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# PC UNITS
def add_pc(pc_name):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO pc_units (pc_name, status) VALUES (%s,'AVAILABLE')", (pc_name,))
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def list_available_pc():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pc_units WHERE status = 'AVAILABLE' ORDER BY pc_name")
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def list_pc_status():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pc_units ORDER BY pc_name")
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def assign_pc(pc_name):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE pc_units SET status = 'IN-USE' WHERE pc_name = %s AND status = 'AVAILABLE'", (pc_name,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def free_pc(pc_name):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE pc_units SET status = 'AVAILABLE' WHERE pc_name = %s", (pc_name,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# VISITS
def get_open_visit(student_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM library_visits WHERE student_id = %s AND status = 'INSIDE' ORDER BY visit_id DESC LIMIT 1", (student_id,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def time_in_visit(student_id, visit_date, time_in, book_id, using_pc, pc_name, points_earned):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO library_visits (student_id, visit_date, time_in, book_id, using_pc, pc_name, points_earned, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,'INSIDE')
            """,
            (student_id, visit_date, time_in, book_id, using_pc, pc_name, points_earned),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def start_pc_usage(visit_id, student_id, pc_name, time_start):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO pc_usage (visit_id, student_id, pc_name, time_start, status) VALUES (%s,%s,%s,%s,'USING')",
            (visit_id, student_id, pc_name, time_start),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def time_out_visit(visit_id, time_out):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE library_visits SET time_out = %s, status = 'OUT' WHERE visit_id = %s", (time_out, visit_id))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def end_pc_usage(visit_id, time_end):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE pc_usage SET time_end = %s, status = 'DONE' WHERE visit_id = %s AND status = 'USING'", (time_end, visit_id))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_inside_visits():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT v.visit_id, v.student_id, s.full_name, s.grade_level, s.section, v.visit_date, v.time_in, v.book_id, v.using_pc, v.pc_name
            FROM library_visits v
            JOIN students s ON s.student_id = v.student_id
            WHERE v.status = 'INSIDE'
            ORDER BY v.time_in ASC
            """,
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_leaderboard():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT student_id, full_name, grade_level, section, total_visits, total_points FROM students ORDER BY total_points DESC, total_visits DESC LIMIT 10")
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_student_history(student_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT v.visit_id, v.visit_date, v.time_in, v.time_out, v.book_id, b.title, v.using_pc, v.pc_name, v.points_earned, v.status
            FROM library_visits v
            LEFT JOIN books b ON b.book_id = v.book_id
            WHERE v.student_id = %s
            ORDER BY v.visit_date DESC, v.visit_id DESC
            """,
            (student_id,),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# UPDATE FUNCTIONS
def update_student(student_id, full_name, grade_level, section):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET full_name=%s, grade_level=%s, section=%s WHERE student_id=%s",
            (full_name, grade_level, section, student_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def update_book(book_id, title, author):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE books SET title=%s, author=%s WHERE book_id=%s",
            (title, author, book_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def update_pc_name(old_pc_name, new_pc_name):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE pc_units SET pc_name=%s WHERE pc_name=%s", (new_pc_name, old_pc_name))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# DELETE FUNCTIONS
def count_student_visits(student_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM library_visits WHERE student_id=%s", (student_id,))
        res = cursor.fetchone()
        return res[0] if res else 0
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def count_book_visits(book_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM library_visits WHERE book_id=%s", (book_id,))
        res = cursor.fetchone()
        return res[0] if res else 0
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def find_pc(pc_name):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pc_units WHERE pc_name=%s", (pc_name,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_student(student_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_book(book_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_pc(pc_name):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM pc_units WHERE pc_name=%s", (pc_name,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
