import hashlib
import bcrypt
import json

# Password and salt for testing/demo purposes
password = "123"
salt = "s@lt"

# Generate hashes
md5_hash = hashlib.md5(password.encode()).hexdigest()
sha256_salted = hashlib.sha256((password + salt).encode()).hexdigest()
bcrypt_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Store everything in a dictionary
hashes = {
    "password": password,               
    "salt": salt,
    "md5": md5_hash,
    "sha256_salted": sha256_salted,
    "bcrypt": bcrypt_hash
}

#Save to passwords.json
with open("passwords.json", "w") as f:
    json.dump(hashes, f, indent=4)

# Print for visual confirmation
print("Hashes saved to passwords.json")
print("MD5:            ", md5_hash)
print("SHA256 + salt:  ", sha256_salted)
print("bcrypt:         ", bcrypt_hash)
