import secrets
import string

# Define the character sets
def gen_password():
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password_length = 12

    password = ''.join(secrets.choice(all_characters) for i in range(password_length))
    return password



