from flask import Flask, request, render_template
import json

app = Flask(__name__)  # ✅ use name, not name

# Load user data
with open("users.json") as f:
    users = json.load(f)

@app.route("/login.php", methods=["GET", "POST"])  # URL looks like PHP to fool Hydra
def login():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("pass")

        if username in users and users[username] == password:
            return "Welcome!"
        else:
            return "incorrect"  # important for Hydra's F= flag

    return render_template("login.html")

if __name__ == "__main__":  # fix typo
    app.run(host="0.0.0.0", port=80)  # optional: allow external access from Hydra
