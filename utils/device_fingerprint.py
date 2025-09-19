# Generating a Device Fingerprint
import hashlib

def generate_device_fingerprint(user_agent: str, ip: str) -> str:
    raw_string = f"{user_agent}-{ip}"
    return hashlib.sha256(raw_string.encode()).hexdigest()
