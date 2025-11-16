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

git clone https://github.com/lllyasviel/stable-diffusion-webui-forge.git

# 実行用一般ユーザーを作成
useradd -m -s /bin/bash user && su - user
usermod -aG sudo user
su - user
cd /workspace/stable-diffusion-webui-forge

echo "You can now run: bash webui.sh --listen --port 7860"
