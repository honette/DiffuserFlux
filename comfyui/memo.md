## RunPod 上で ComfyUI を手動構築する手順

理由がない限り公式のPodテンプレートを使ったほうが良い

### 1. Pod に入る

- GPUメモリ48GB以上のPodを選択
- Podテンプレートは `Runpod Pytorch 2.8.0` もしくは `My Flux Kontext`
- Expose HTTP Portsに8188を追加 `8188,8888`

---

### 2. 依存関係をインストール

まず Python と git があることを確認します。なければインストール：

```bash
apt update && apt install -y python3 python3-venv python3-pip git
```

（Pod のベースイメージによっては最初から入ってることも多いです）

---

### 3. ComfyUI を取得

```bash
cd /workspace
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

---

### 4. 仮想環境を作成・有効化

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 5. 依存パッケージをインストール

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 6. ComfyUI を起動

```bash
python main.py --listen 0.0.0.0 --port 8188
```
- PodのConnectから `ComfyUI` を開く