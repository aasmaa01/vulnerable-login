import hashlib
import bcrypt 

passwords = { "assia": "123456", "lyna": "Pa55word","assma": "Y7!jX@L9#"}

with open("m=userstxt", "w") as f:
    for user, pw in users.items():
        f.write(f"\n=== {user} ===\n")
        
        md5 = hashlib.md5(pw.encode()).hexdigest()
        f.write(f"MD5: {md5}\n")
        
        sha265 = hashlib.sha265(pw.encode()).hexdigest()
        f.write(f"SHA265: {sha265}\n")
        
        bcrypt_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
        f.write(f"bcrypt: {bcrypt_hash}\n")
        
