import hashlib
import itertools
import string

# Define password space and limits
CHARSET = string.ascii_letters + string.digits + "!@#"
MAX_LENGTH = 9  # Max brute-force length (adjusted to your request)

# Load users and their hashes
def load_hashes(file_path):
    users = {}
    current_user = None
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("==="):
                current_user = line.strip("= ").lower()
                users[current_user] = {}
            elif ":" in line:
                hash_type, value = line.split(":", 1)
                users[current_user][hash_type.strip().lower()] = value.strip()
    return users

# Brute force for MD5 or SHA256
def crack_hash(target_hash, hash_type):
    for length in range(1, MAX_LENGTH + 1):
        for attempt in itertools.product(CHARSET, repeat=length):
            pwd = ''.join(attempt)
            if hash_type == "md5":
                candidate_hash = hashlib.md5(pwd.encode()).hexdigest()
            elif hash_type == "sha256":
                candidate_hash = hashlib.sha256(pwd.encode()).hexdigest()
            else:
                return None

            if candidate_hash == target_hash:
                return pwd
    return None

# Main (bcrypt skipped)
if __name__ == "__main__":
    users = load_hashes("users.txt")
    print("\n Starting brute-force cracking (MD5 + SHA256 only)...\n")

    for user, hashes in users.items():
        print(f"User: {user.capitalize()}")

        # Crack MD5
        if "md5" in hashes:
            result = crack_hash(hashes["md5"], "md5")
            print(f"  MD5     → {result if result else 'Not found'}")

        # Crack SHA-256
        if "sha256" in hashes:
            result = crack_hash(hashes["sha256"], "sha256")
            print(f"  SHA256  → {result if result else 'Not found'}")

        print()
