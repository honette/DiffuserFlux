FROM runpod/pytorch:1.0.1-cu1281-torch280-ubuntu2404

RUN apt update && apt install -y \
    vim nano htop less tree wget curl git python3-venv zip unzip p7zip-full tar gzip bzip2 xz-utils \
    && echo "alias ll='ls -lh --color=auto'" >> /etc/bash.bashrc

WORKDIR /workspace

RUN git clone https://github.com/honette/DiffuserFlux.git /workspace/DiffuserFlux

WORKDIR /workspace/DiffuserFlux
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["/bin/bash"]
