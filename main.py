from database import *
from auth import *

def askUser(token):
    while True:
        user = requireRole(token, ["USER", "SUPER_ADMIN"])
        if not user:
            return
        userInput = input("""
            Enter choice:
            1. View all students
            2. Insert new student
            3. Get student by ID
            4. Update student
            5. Delete Student
            9. Stop
            Choice: """)
        match userInput:
            case "1":
                if requireRole(token, ["USER", "SUPER_ADMIN"]):
                    selectAllStudents()
            case "2":
                if requireRole(token, ["USER", "SUPER_ADMIN"]):
                    addNew()
            case "3":
                if requireRole(token, ["USER", "SUPER_ADMIN"]):
                    getStudentById()
            case "4":
                if requireRole(token, ["USER", "SUPER_ADMIN"]):
                    updateStudent()
            case "5":
                if requireRole(token, ["USER", "SUPER_ADMIN"]):
                    deleteStudent() 
            case "9":
                logout(token)
                return
            case _:
                print("Invalid choice")

def selectAllStudents():
    students = fetchAllStudents();
    if students:
        print("\n".join(str(value) for value in students))
    else:
        print("\n no data")

def validateEmail(email):
    if email and "@" in email:
        return True
    return False

def validatePhone(phone):
    if phone.isdigit() and len(phone) == 10:
        return True
    return False

def validateAge(age):
    if age.isdigit() and 0 < int(age) <= 150:
        return True
    return False

def validateLen(strVal):
    if strVal and len(strVal.strip()) > 0:
        return True
    return False

def addNew():
    name = input("Enter student name: ").strip()
    if not validateLen(name):
        print("Invalid name")
        return
    email = input("Enter email: ").strip()
    if not validateEmail(email):
        print("Invalid email")
        return
    phone = input("Enter phone number: ").strip()
    if not validatePhone(phone):
        print("Invalid phone number")
        return
    age = input("Enter age: ").strip()
    if not validateAge(age):
        print("Invalid age")
        return
    course = input("Enter course: ").strip()
    if not validateLen(course):
        print("Invalid course")
        return
    address = input("Enter address: ").strip()
    if not validateLen(address):
        print("Invalid address")
        return
    insertData(name, email, phone, age, course, address)

def getStudentById():
    studentId = input("Enter student id:   ")
    if not studentId.isdigit() or int(studentId) <= 0:
        print("Invalid student ID")
        return
    student=getStudentDataById(studentId)
    if student:
        print(student)
    else:
        print("Student not found")

def deleteStudent():
    studentId = input("Enter student id:   ")
    if not studentId.isdigit() or int(studentId) <= 0:
        print("Invalid student ID")
        return
    deleteStudentData(studentId)

def updateStudent():
    studentId = input("Enter student id:   ")
    if not studentId.isdigit() or int(studentId) <= 0:
        print("Invalid student ID")
        return
    name = input("Enter student name: ").strip()
    if not validateLen(name):
        print("Invalid name")
        return
    email = input("Enter email: ").strip()
    if not validateEmail(email):
        print("Invalid email")
        return
    phone = input("Enter phone number: ").strip()
    if not validatePhone(phone):
        print("Invalid phone number")
        return
    age = input("Enter age: ").strip()
    if not validateAge(age):
        print("Invalid age")
        return
    course = input("Enter course: ").strip()
    if not validateLen(course):
        print("Invalid course")
        return
    address = input("Enter address: ").strip()
    if not validateLen(address):
        print("Invalid address")
        return
    updateStudentData(studentId,name, email, phone, age, course, address)

# askUser()

def userManagement():
    while True:
        userInput = input("""
            Enter choice:
            1. Register new user
            2. Login existing user
            3. Stop
            Choice: """)
        match userInput:
            case "1":
                registerUser()
            case "2":
                session = loginUser()
                if session:
                    print("Login successful")
                    print("Welcome,", session["name"])
                    
                    if session["role"] == "SUPER_ADMIN":
                        adminMenu(session["token"])
                    else:
                        askUser(session["token"])
            case "3":
                print("Goodbye!")
                break
            case _:
                print("Invalid choice")

def registerUser():
    name = input("Enter name: ").strip()
    if not validateLen(name):
        print("Invalid name")
        return
    email = input("Enter email: ").strip()
    if not validateEmail(email):
        print("Invalid email")
        return
    if(checkWhetherEmailExist(email)):
        print("Already exist email id ,please try with different email")
        return
    password = input("Enter password: ").strip()
    if not validateLen(password):
        print("Invalid password")
        return
    password_hash=hashPassword(password)
    insertUser(name, email, password_hash)

def loginUser():
    email = input("Enter email: ").strip()
    if not validateEmail(email):
        print("Invalid email")
        return
    password = input("Enter password: ").strip()
    if not validateLen(password):
        print("Invalid password")
        return
    user = fetchUserByEmail(email)

    if not user:
        print("Invalid email or password.")
        return

    user_id = user[0]
    name = user[1]
    password_hash = user[3]
    role = user[4]

    if not verifyPassword(password, password_hash):
        print("Invalid email or password.")
        return

    token, token_hash, expires_at = generateToken()

    if not saveAuthToken(user_id, token_hash, expires_at):
        print("Unable to create login session.")
        return

    print("Login successful")

    userSession = {
        "user_id": user_id,
        "name": name,
        "role": role,
        "token": token,
        "expires_at": expires_at
    }

    return userSession

# def selectAllUsers():
#     users = fetchAllUsers();
#     if users:
#         print("\n".join(str(value) for value in users))
#     else:
#         print("\n no data")


def adminMenu(token):
    while True:
        admin = requireRole(token, ["SUPER_ADMIN"])

        if not admin:
            return

        userInput = input("""
            Super Admin Menu
            1. View all users
            2. Create user
            3. Update user
            4. Delete user
            9. Logout
            Choice: """)

        match userInput:
            case "1":
                selectAllUsers(token)

            case "2":
                createNormalUser(token)
                pass

            case "3":
                updateNormalUser(token)
                pass

            case "4":
                deleteNormalUser(token)
                pass

            case "9":
                logout(token)
                return

            case _:
                print("Invalid choice")

def selectAllUsers(token):
    admin = requireRole(token, ["SUPER_ADMIN"])

    if not admin:
        return

    users = fetchAllUserDetails()

    if users:
        for user in users:
            # Avoid printing password hashes and tokens.
            print(user)
    else:
        print("No users found.")



def logout(token):
    user = validateToken(token)

    if not user:
        print("Session is already invalid or expired.")
        return

    if clearAuthToken(token):
        print("Logged out successfully.")
    else:
        print("Unable to log out.")

def createNormalUser(token):
    admin = requireRole(token, ["SUPER_ADMIN"])

    if not admin:
        return

    name = input("Enter name: ").strip()
    if not validateLen(name):
        print("Invalid name")
        return

    email = input("Enter email: ").strip()
    if not validateEmail(email):
        print("Invalid email")
        return

    if checkWhetherEmailExist(email):
        print("Email already exists.")
        return

    password = input("Enter password: ")
    if not password:
        print("Invalid password")
        return

    password_hash = hashPassword(password)

    insertUser(name, email, password_hash, role="USER")



def updateNormalUser(token):
    admin = requireRole(token, ["SUPER_ADMIN"])
    if not admin:
        return

    email = input("Enter user email to update: ").strip()
    if not validateEmail(email):
        print("Invalid email")
        return

    name = input("Enter new name: ").strip()
    if not validateLen(name):
        print("Invalid name")
        return

    newEmail = input("Enter new email: ").strip()
    if not validateEmail(newEmail):
        print("Invalid email")
        return

    password_hash = None
    change_password = input("Change password? (y/n): ").strip().lower()

    if change_password == "y":
        from getpass import getpass
        password = getpass("Enter new password: ")
        if not password:
            print("Invalid password")
            return
        password_hash = hashPassword(password)

    updated = updateNormalUserData(
        email, name, newEmail, password_hash
    )

    if updated:
        print("User updated successfully.")
    else:
        print("User not found or cannot be modified.")


def deleteNormalUser(token):
    admin = requireRole(token, ["SUPER_ADMIN"])
    if not admin:
        return

    email = input("Enter user email to delete: ").strip()
    if not validateEmail(email):
        print("Invalid user ID")
        return

    deleted = deleteNormalUserData(email)

    if deleted:
        print("User deleted successfully.")
    else:
        print("User not found or cannot be deleted.")


userManagement()
