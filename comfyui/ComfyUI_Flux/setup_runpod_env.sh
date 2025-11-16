#!/bin/bash
# ==========================================
# setup_runpod_env.sh
# RunPod ComfyUI 環境初期化スクリプト
# ==========================================

set -e

echo "🚀 Setting up DiffuserFlux + ComfyUI environment..."

apt update && apt install -y python3 python3-venv python3-pip git vim rsync

cd /workspace

# リポジトリを取得
if [ ! -d "DiffuserFlux" ]; then
  echo "📦 Cloning DiffuserFlux..."
  git clone https://github.com/honette/DiffuserFlux.git
else
  echo "🔁 DiffuserFlux already exists, skipping clone."
fi

# Python依存パッケージをインストール
cd /workspace/DiffuserFlux/comfyui
echo "📦 Installing Python dependencies..."
pip install -U pip tqdm gdown

python3 /workspace/DiffuserFlux/comfyui/ComfyUI_Flux/download_models.py

# ComfyUI Manager > Mod Manager >REFRESH