#!/bin/bash
# ============================================
# Download LoRA safetensors from Google Drive
# ============================================

# JD3s_Nudify_Kontext
FILE_ID="1LJ9Xa2BrvT8i2h_sr_oBEbDDZdEWn4U6"
# NSFW V3
#FILE_ID="1evQqmVHCpDNRM4ehiA-SVlpFUUkOSvpr"
# FLUXTASTIC_V3
#FILE_ID="1oblgf_aC6qDjg-5A3MswVfqWqEKxuoFO"

OUT_DIR="/workspace/DiffuserFlux"
OUT_FILE="${OUT_DIR}/lora_model.safetensors"

mkdir -p "${OUT_DIR}"

echo "Downloading LoRA from Google Drive..."
echo "Target: ${OUT_FILE}"

wget --no-check-certificate \
  "https://drive.google.com/uc?export=download&id=${FILE_ID}" \
  -O "${OUT_FILE}"

if [ $? -eq 0 ]; then
  echo "✅ Download complete: ${OUT_FILE}"
else
  echo "❌ Download failed!"
  exit 1
fi
