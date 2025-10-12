#!/bin/bash
# ========== auto_sync.sh ==========
# RunPod の ComfyUI 出力を定期的に同期する
# 実行例: ./auto_sync.sh 69.30.85.57 22092

IP="$1"
PORT="$2"
KEY_PATH=~/.ssh/id_runpod
REMOTE_DIR=/workspace/runpod-slim/ComfyUI/output/video/
LOCAL_DIR=/mnt/g/AI/source_images/_vid/output/
INTERVAL=300   # 秒（5分ごと）

mkdir -p "$LOCAL_DIR"

echo "🕓 Starting auto rsync loop every ${INTERVAL}s"
echo "🔗 From: root@${IP}:${REMOTE_DIR}"
echo "📥 To:   ${LOCAL_DIR}"

while true; do
  echo "🔄 $(date '+%Y-%m-%d %H:%M:%S') — syncing..."
  rsync -avz --progress -e "ssh -i ${KEY_PATH} -p ${PORT}" \
    root@"${IP}":"${REMOTE_DIR}" "${LOCAL_DIR}"
  sleep "$INTERVAL"
done
