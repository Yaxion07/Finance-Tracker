from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function for hashing password.
def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)
