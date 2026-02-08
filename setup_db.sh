#!/data/data/com.termux/files/usr/bin/bash

set -e

DB_NAME="password_vault"
DB_USER="vault_user"
DB_PASS="CHANGE_THIS_PASSWORD"

echo "[*] Installing MariaDB..."
pkg install -y mariadb

echo "[*] Initializing database (first run only)..."
if [ ! -d "$PREFIX/var/lib/mysql/mysql" ]; then
    mysql_install_db
fi

echo "[*] Starting MariaDB..."
mysqld_safe --datadir=$PREFIX/var/lib/mysql &

# wait for mysql socket
sleep 5

echo "[*] Creating database and tables..."

mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS ${DB_NAME};

CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;

USE ${DB_NAME};

CREATE TABLE IF NOT EXISTS credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    website VARCHAR(255) NOT NULL,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARBINARY(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
EOF

echo "[✓] Database setup complete."
echo "    DB: ${DB_NAME}"
echo "    User: ${DB_USER}"
