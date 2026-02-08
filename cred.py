import os
import subprocess
import getpass
import shlex

DB = "password_vault"
AES_KEY = os.getenv("VAULT_AES_KEY")

if not AES_KEY:
    raise SystemExit("VAULT_AES_KEY not set")

def run_sql(sql):
    cmd = [
        "mariadb",
        DB,
        "-e",
        sql
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("❌ SQL ERROR")
        print(result.stderr)
        return False

    if result.stdout:
        print(result.stdout)

    return True

def esc(val):
    return val.replace("\\", "\\\\").replace("'", "\\'")

def add_entry():
    website = esc(input("Website  : "))
    username = esc(input("Username : "))
    email = esc(input("Email    : "))
    password = esc(getpass.getpass("Password : "))

    sql = f"""
    INSERT INTO credentials (website, username, email, password)
    VALUES (
        '{website}',
        '{username}',
        '{email}',
        AES_ENCRYPT('{password}', '{AES_KEY}')
    );
    """

    if run_sql(sql):
        print("✔ Stored")

def view_entries():
    sql = f"""
    SELECT website, username, email,
    CAST(AES_DECRYPT(password, '{AES_KEY}') AS CHAR) AS password
    FROM credentials
    ORDER BY created_at DESC;
    """
    run_sql(sql)

def menu():
    while True:
        print("\n1. Add password")
        print("2. View passwords")
        print("3. Exit")

        c = input("Choose: ")
        if c == "1":
            add_entry()
        elif c == "2":
            view_entries()
        elif c == "3":
            break

menu()
