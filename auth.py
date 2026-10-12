import bcrypt
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from database import *

def hashPassword(password):
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verifyPassword(password, password_hash):
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)


def generateToken():
    # Generate a cryptographically secure random token
    token = secrets.token_urlsafe(32)

    # Store a hash of the token in the database
    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    # Token expires after 30 minutes
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)

    return token, token_hash, expires_at

#######################################


def validateToken(token):
    if not token:
        print("Token is missing.")
        return None

    # Hash the token received from the application
    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    # Find the user associated with this token
    user = fetchUserByTokenHash(token_hash)

    if not user:
        print("Invalid token.")
        return None

    user_id = user[0]
    name = user[1]
    email = user[2]
    role = user[3]
    expires_at = user[4]

    # Check whether the token has an expiry time
    if expires_at is None:
        print("Token expiry is missing.")
        return None

    # Handle both TIMESTAMP and TIMESTAMPTZ columns
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    # Check whether the token has expired
    if datetime.now(timezone.utc) >= expires_at:
        print("Token has expired.")
        return None

    # Return authenticated user information
    return {
        "user_id": user_id,
        "name": name,
        "email": email,
        "role": role
    }



def requireRole(token, allowed_roles):
    user = validateToken(token)

    if not user:
        print("Authentication failed. Please log in again.")
        return None

    if user["role"] not in allowed_roles:
        print("Access denied. You do not have permission.")
        return None

    return user

def clearAuthToken(token):
    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    try:
        cursor.execute("""
            UPDATE users
            SET auth_token = NULL,
                token_expires_at = NULL
            WHERE auth_token = %s
        """, (token_hash,))

        connection.commit()
        return cursor.rowcount > 0

    except psycopg2.Error as e:
        connection.rollback()
        print("Database error:", e)
        return False
