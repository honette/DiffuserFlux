#!/bin/bash
# ==============================================
# ssh_helper.sh - Show RunPod SSH/Rsync commands
# Usage: sh ssh_helper.sh <IP:PORT>
# Example: sh ssh_helper.sh 69.30.85.30:22044
# ==============================================

if [ -z "$1" ]; then
  echo "Usage: sh ssh_helper.sh <IP:PORT>"
  exit 1
fi

ADDR="$1"
IP="${ADDR%%:*}"
PORT="${ADDR##*:}"

echo ""
echo "SSH / RSYNC helper for RunPod"
echo "----------------------------------"
echo "ssh root@${IP} -p ${PORT} -i ~/.ssh/id_runpod"
echo "rsync -avz -e \"ssh -i ~/.ssh/id_runpod -p ${PORT}\" root@${IP}:/workspace/DiffuserFlux/tmp/ ./"
echo "rsync -avz -e \"ssh -i ~/.ssh/id_runpod -p ${PORT}\" root@${IP}:/workspace/DiffuserFlux/batch/outputs/ ./"
echo "rsync -avz -e \"ssh -i ~/.ssh/id_runpod -p ${PORT}\" root@${IP}:/workspace/runpod-slim/ComfyUI/output/video/ /mnt/g/AI/source_images/_vid/output/"
echo "----------------------------------"
