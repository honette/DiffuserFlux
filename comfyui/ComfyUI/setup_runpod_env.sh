#!/bin/bash
# ==========================================
# setup_runpod_env.sh
# RunPod ComfyUI 環境初期化スクリプト
# ==========================================

set -e

echo "🚀 Setting up DiffuserFlux + ComfyUI environment..."

cd /workspace

# リポジトリを取得
if [ ! -d "DiffuserFlux" ]; then
  echo "📦 Cloning DiffuserFlux..."
  git clone https://github.com/honette/DiffuserFlux.git
else
  echo "🔁 DiffuserFlux already exists, skipping clone."
fi

# Python依存パッケージをインストール
cd DiffuserFlux/comfyui
echo "📦 Installing Python dependencies..."
pip install -U pip tqdm gdown

# モデルのダウンロード
echo "⬇️ Downloading WAN Diffuser model..."
python3 download_wan_diffuser_model_for_comfyui.py
echo "⬇️ Downloading WAN LoRA..."
python3 download_wan_lora.py

# ComfyUI に必要ファイルをコピー
echo "🧩 Copying workflow, images, and scripts to ComfyUI..."
SRC_DIR="/workspace/DiffuserFlux/comfyui/ComfyUI"
DST_DIR="/workspace/runpod-slim/ComfyUI"

mkdir -p "${DST_DIR}/input_images"
mkdir -p "${DST_DIR}/scripts"

cp -r "${SRC_DIR}/api-video_wan2_2_14B_i2v.json" "${DST_DIR}/"
cp -r "${SRC_DIR}/input_images/"* "${DST_DIR}/input_images/" 2>/dev/null || true
cp -r "${SRC_DIR}/scripts/"* "${DST_DIR}/scripts/"
cp -r "${SRC_DIR}/scripts/config_api_i2v_default.json" "${DST_DIR}/scripts/config_api_i2v.json"

# ComfyUI用Python依存パッケージをインストール
echo "📦 Installing ComfyUI script requirements..."
cd "${DST_DIR}/scripts"
pip install -r requirements.txt

# Linuxユーティリティを導入
echo "🧰 Installing rsync and vim..."
apt update -y && apt install -y rsync vim

# ✅ 完了
echo ""
echo "✅ Environment setup complete!"
echo "📁 Files copied to: ${DST_DIR}"
echo "You can now run:"
echo "  cd ${DST_DIR}/scripts"
echo "  python3 batch_api_i2v.py --limit 20 --skip 0"
