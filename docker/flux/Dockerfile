# ---- RunPod公式ベース (SSHやExpose対応済み) ----
FROM runpod/base:1.0.1-cuda1281-ubuntu2404

# ---- 基本ツール追加 ----
RUN apt update && apt install -y \
    vim nano htop less tree wget curl git python3 python3-pip python3-venv \
    zip unzip p7zip-full tar gzip bzip2 xz-utils rsync

# ---- Python / PyTorch 環境構築 ----
RUN pip install --upgrade pip setuptools
RUN pip install torch==2.8.0+cu128 torchvision==0.23.0+cu128 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128

# ---- DiffuserFlux インストール ----
WORKDIR /workspace
RUN git clone https://github.com/honette/DiffuserFlux.git /workspace/DiffuserFlux
WORKDIR /workspace/DiffuserFlux
RUN pip install -r requirements.txt

# ---- 起動コマンド ----
# RunPodベースイメージのentrypointは自動でSSHやhealth agentを起動するので変更不要
CMD ["/bin/bash"]
