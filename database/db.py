import sqlite3
import os
import bcrypt

DATABASE_NAME = os.path.join("database", "jp_arogya_ai.db")


def create_database():

    os.makedirs("database", exist_ok=True)

    con = sqlite3.connect(DATABASE_NAME)

    cur = con.cursor()

    # USERS

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT UNIQUE,

        password TEXT

    )
    """)

    # CHAT

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_email TEXT,

        question TEXT,

        answer TEXT

    )
    """)

    # REPORTS

    cur.execute("""
    CREATE TABLE IF NOT EXISTS medical_reports(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_email TEXT,

        filename TEXT,

        report_text TEXT,

        analysis TEXT

    )
    """)

    con.commit()

    con.close()

    print("✅ Database Created Successfully!")


# REGISTER

def register_user(name, email, password):

    con = sqlite3.connect(DATABASE_NAME)

    cur = con.cursor()

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    try:

        cur.execute(
            """
            INSERT INTO users
            (name,email,password)
            VALUES(?,?,?)
            """,
            (
                name,
                email,
                hashed
            )
        )

        con.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        con.close()


# LOGIN

def login_user(email, password):

    con = sqlite3.connect(DATABASE_NAME)

    cur = con.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    user = cur.fetchone()

    con.close()

    if user is None:

        return None

    if bcrypt.checkpw(
        password.encode(),
        user[3].encode()
    ):

        return user

    return None


# SAVE CHAT

def save_chat(user_email, question, answer):

    con = sqlite3.connect(DATABASE_NAME)

    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO chat_history
        (user_email,question,answer)
        VALUES(?,?,?)
        """,
        (
            user_email,
            question,
            answer
        )
    )

    con.commit()

    con.close()


# GET CHAT

def get_chat_history(user_email):

    con = sqlite3.connect(DATABASE_NAME)

    cur = con.cursor()

    cur.execute(
        """
        SELECT question,answer
        FROM chat_history
        WHERE user_email=?
        ORDER BY id DESC
        """,
        (user_email,)
    )

    data = cur.fetchall()

    con.close()

    return data


# SAVE REPORT

def save_report(user_email, filename, report_text, analysis):

    con = sqlite3.connect(DATABASE_NAME)

    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO medical_reports
        (user_email,filename,report_text,analysis)
        VALUES(?,?,?,?)
        """,
        (
            user_email,
            filename,
            report_text,
            analysis
        )
    )

    con.commit()

    con.close()


# GET REPORTS

def get_reports(user_email):

    con = sqlite3.connect(DATABASE_NAME)

    cur = con.cursor()

    cur.execute(
        """
        SELECT filename,analysis
        FROM medical_reports
        WHERE user_email=?
        ORDER BY id DESC
        """,
        (user_email,)
    )

    data = cur.fetchall()

    con.close()

    return data