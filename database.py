import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="student_management",
    user="postgres",
    password="admin",
    port="5432"
)

cursor = connection.cursor()

def fetchAllStudents():
    try:
        cursor.execute("SELECT * FROM students")
        return cursor.fetchall()
    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)

def insertData(name, email, phone, age, course, address):
    try:
        query = """
        INSERT INTO students
            (name, email, phone, age, course, address)
        VALUES
            (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        cursor.execute(query, (name, email, phone, age, course, address))
        student_id = cursor.fetchone()[0]
        print(f"\nStudent added successfully!")
        print(f"Student ID: {student_id}")
        connection.commit()
    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)    

def getStudentDataById(studentId):
    try:
        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (studentId,)
        )
        return cursor.fetchone()
    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)

def updateStudentData(studentId,name, email, phone, age, course, address):
    try:
        cursor.execute("""
            UPDATE students
            SET
                name = %s,
                email = %s,
                phone = %s,
                age = %s,
                course = %s,
                address = %s
            WHERE id = %s
        """, (
            name,
            email,
            phone,
            age,
            course,
            address,
            studentId
        ))

        connection.commit()

        if cursor.rowcount > 0:
            print("Student updated successfully.")
        else:
            print("Student not found.")
    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)  

def deleteStudentData(studentId):
    try:
        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (studentId,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            print("Student deleted successfully.")
        else:
            print("Student not found.")
    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)  

def checkWhetherEmailExist(email):
    try:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        if cursor.fetchone():
                return True
        return False
    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)
        return True

def insertUser(name, email, password_hash, role="USER"):
    try:
        query = """
            INSERT INTO users
                (name, email, password_hash, role)
            VALUES
                (%s, %s, %s, %s)
            RETURNING id
        """
        cursor.execute(
            query,
            (name, email, password_hash, role)
        )
        user_id = cursor.fetchone()[0]
        connection.commit()
        print("User created successfully.")
        print(f"User ID: {user_id}")
        return user_id

    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)
        return None

def fetchUserByEmail(email):
    try:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        return cursor.fetchone()
    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)
        return None

def fetchAllUsers():
    try:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)

def fetchAllUserDetails():
    try:
        cursor.execute("""SELECT id, name, email, role, created_at
            FROM users
            ORDER BY id""")
        return cursor.fetchall()
    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)
        
def saveAuthToken(id, token_hash, expires_at):
    try:
        cursor.execute("""
            UPDATE users
            SET
                auth_token = %s,
                token_expires_at = %s
            WHERE id= %s
        """, (token_hash, expires_at, id))

        connection.commit()
        return cursor.rowcount > 0

    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)
        return False

def fetchUserByTokenHash(token_hash):
    try:
        cursor.execute("""
            SELECT id, name, email, role, token_expires_at
            FROM users
            WHERE auth_token = %s
        """, (token_hash,))

        return cursor.fetchone()

    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)
        return None

def updateNormalUserData(email, name, newEmail, password_hash=None):
    try:
        if password_hash:
            cursor.execute("""
                UPDATE users
                SET name = %s,
                    email = %s,
                    password_hash = %s
                WHERE email = %s AND role = 'USER'
            """, (name, newEmail, password_hash,email))
        else:
            cursor.execute("""
                UPDATE users
                SET name = %s,
                    email = %s
                WHERE email = %s AND role = 'USER'
            """, (name, newEmail, email))

        connection.commit()
        return cursor.rowcount > 0

    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)
        return False

def deleteNormalUserData(email):
    try:
        cursor.execute("""
            DELETE FROM users
            WHERE email = %s AND role = 'USER'
        """, (email,))

        connection.commit()
        return cursor.rowcount > 0

    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)
        return False
