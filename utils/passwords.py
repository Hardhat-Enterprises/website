import secrets
import string

# Define the character set
def gen_password():
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    special = string.punctuation

    # Ensure password has at least one of each type of character
    password = [
        secrets.choice(upper),    # At least one uppercase letter
        secrets.choice(lower),    # At least one lowercase letter
        secrets.choice(digits),   # At least one digit
        secrets.choice(special)   # At least one special character
    ]

    # Fill the rest of the password with random characters from all character sets
    all_characters = upper + lower + digits + special
    password += [secrets.choice(all_characters) for _ in range(8)]  # Total length 12

    # Shuffle the password list to ensure randomness
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)
