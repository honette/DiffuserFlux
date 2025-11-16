#!/bin/bash
set -e  # 途中でエラーが出たら止まるようにする

# === 1. File Browser のインストール（初回のみ） ===
if ! command -v filebrowser &> /dev/null; then
    echo "[+] Installing File Browser..."
    curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash
else
    echo "[+] File Browser already installed."
fi

# === 2. パスワード初期化（初回のみ実行） ===
if [ ! -f /workspace/filebrowser.db ]; then
    echo "[+] Initializing File Browser user database..."
    filebrowser -d /workspace/filebrowser.db users add admin adminadminadmin --perm.admin
else
    echo "[+] Using existing database: /workspace/filebrowser.db"
fi

# === 3. File Browser の起動 ===
echo "[+] Starting File Browser..."
nohup filebrowser -r /workspace -a 0.0.0.0 -p 8080 --database /workspace/filebrowser.db >/workspace/filebrowser.log 2>&1 &
echo "[+] File Browser is running on port 8080"
