#!/usr/bin/env python3
import paramiko, subprocess, sys, time, argparse, os, datetime

parser = argparse.ArgumentParser(description="Remote multi-batch controller (always resume + rsync)")
parser.add_argument("target", help="接続先IP:ポート (例: 63.141.33.29:22020)")
parser.add_argument("--user", default="root", help="SSHユーザー名 (デフォルト: root)")
parser.add_argument("--key", default="~/.ssh/id_runpod", help="SSH秘密鍵のパス")
parser.add_argument("--total", type=int, required=True, help="処理する総ファイル数")
parser.add_argument("--limit", type=int, default=20, help="1回あたりの処理数（固定推奨）")
args = parser.parse_args()

# ==== 接続情報 ====
ip, port = args.target.split(":")
port = int(port)

# ==== ログセットアップ ====
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, f"run_{ip.replace('.', '_')}_{timestamp}.log")

def log(msg):
    print(msg)
    with open(log_path, "a") as f:
        f.write(msg + "\n")

log(f"🕓 Start {timestamp} | Target={ip}:{port} | limit={args.limit}, total={args.total}")

# ==== SSH接続 ====
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(ip, port=port, username=args.user, key_filename=os.path.expanduser(args.key))
except Exception as e:
    log(f"❌ SSH接続失敗: {e}")
    sys.exit(1)

# ==== バッチ数 ====
batches = (args.total + args.limit - 1) // args.limit
log(f"📦 Total {args.total} files → {batches} batches")

# ==== 実行ループ ====
for i in range(batches):
    skip = i * args.limit
    cmd = (
        f"cd /workspace/runpod-slim/ComfyUI/scripts && "
        f"python3 batch_i2v_resume.py --limit {args.limit} --skip {skip} --resume"
    )

    log(f"\n🚀 [Batch {i+1}/{batches}] Executing: {cmd}")

    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line, end="")
        with open(log_path, "a") as f:
            f.write(line)

    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        log(f"✅ Batch {i+1}/{batches} completed OK")
    else:
        log(f"⚠️ Batch {i+1}/{batches} failed with exit code {exit_status}")
        break

    # ==== rsyncで結果同期 ====
    local_outdir = os.path.join("output", ip)
    os.makedirs(local_outdir, exist_ok=True)
    rsync_cmd = [
        "rsync", "-avz", "--progress",
        "-e", f"ssh -p {port} -i {os.path.expanduser(args.key)}",
        f"{args.user}@{ip}:/workspace/runpod-slim/ComfyUI/video/ComfyUI/",
        f"{local_outdir}/"
    ]
    log(f"⬇️ Rsync output: {' '.join(rsync_cmd)}")
    subprocess.run(rsync_cmd)

    if i < batches - 1:
        log("⏸️ Waiting 5s before next batch ...")
        time.sleep(5)

ssh.close()
log("🏁 All batches finished.")
