FROM runpod/pytorch:1.0.1-cu1281-torch280-ubuntu2404

RUN apt update && apt install -y \
    vim nano htop less tree wget curl git python3-venv zip unzip p7zip-full tar gzip bzip2 xz-utils \
    && echo "alias ll='ls -lh --color=auto'" >> /etc/bash.bashrc

WORKDIR /workspace

RUN git clone https://github.com/comfyanonymous/ComfyUI.git /workspace/ComfyUI
WORKDIR /workspace/ComfyUI
RUN python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8188/ || exit 1

CMD ["/bin/bash", "-c", "cd /workspace/ComfyUI && source venv/bin/activate && python main.py --listen 0.0.0.0 --port 8188"]
