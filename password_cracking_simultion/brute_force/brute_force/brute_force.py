import hashlib
import itertools
import string
import bcrypt
import time
import json

# Load hashes
with open("passwords.json") as f:
    data = json.load(f)

target_md5 = data["md5"]
target_sha256_salted = data["sha256_salted"]
salt = data["salt"]
bcrypt_hash = data["bcrypt"].encode()

# Brute-force config
CHARSET = string.ascii_lowercase + string.digits
MAX_LENGTH = 5

def crack_hash(target, hash_type, salt=""):
    print(f"\nCracking {hash_type.upper()}...")
    start_time = time.time()
    attempts = 0
    hash_times = []

    for length in range(1, MAX_LENGTH + 1):
        for attempt in itertools.product(CHARSET, repeat=length):
            pwd = ''.join(attempt)
            pwd_to_check = pwd + salt if salt else pwd

            t0 = time.time()
            if hash_type == "md5":
                hashed = hashlib.md5(pwd_to_check.encode()).hexdigest()
            elif hash_type == "sha256":
                hashed = hashlib.sha256(pwd_to_check.encode()).hexdigest()
            else:
                continue
            t1 = time.time()

            hash_times.append(t1 - t0)
            attempts += 1

            if hashed == target:
                duration = time.time() - start_time
                avg_time = sum(hash_times) / len(hash_times)
                print(f"Found: {pwd} in {duration:.2f}s after {attempts} attempts (avg time: {avg_time:.6f}s)")
                return pwd

    print("Password not found.")
    return None

def try_bcrypt_bruteforce(target_bcrypt, timeout_seconds=5):
    print("\nAttempting bcrypt brute-force (limited time)...")
    start = time.time()
    attempts = 0

    for length in range(1, MAX_LENGTH + 1):
        for attempt in itertools.product(CHARSET, repeat=length):
            if time.time() - start > timeout_seconds:
                print(f"Timeout reached after {timeout_seconds}s and {attempts} attempts.")
                return

            pwd = ''.join(attempt)
            attempts += 1

            if bcrypt.checkpw(pwd.encode(), target_bcrypt):
                print(f"Found bcrypt password: {pwd}")
                return

    print("bcrypt password not found in time limit.")

if __name__ == "__main__":
    print("Loaded hashes from passwords.json")
    print(f"Charset: {CHARSET}")
    print(f"Max length: {MAX_LENGTH}")

    crack_hash(target_md5, "md5")
    crack_hash(target_sha256_salted, "sha256", salt=salt)

    if bcrypt_hash.startswith(b"$2b$") or bcrypt_hash.startswith(b"$2a$"):
        try_bcrypt_bruteforce(bcrypt_hash, timeout_seconds=5)
    
