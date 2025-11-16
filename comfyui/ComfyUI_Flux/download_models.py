import os
import requests
from tqdm import tqdm

# 保存先ベースパス
BASE_DIR = "/workspace/runpod-slim/ComfyUI"

# Hugging Face トークンを環境変数から取得
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("環境変数 HF_TOKEN が設定されていません！")

# 認証ヘッダ
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# ダウンロード対象ファイル
files = {
    "models/diffusion_models/flux1-krea-dev_fp8_scaled.safetensors":
        "https://huggingface.co/Comfy-Org/FLUX.1-Krea-dev_ComfyUI/resolve/main/split_files/diffusion_models/flux1-krea-dev_fp8_scaled.safetensors",
    "models/text_encoders/clip_l.safetensors":
        "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors",
    "models/text_encoders/t5xxl_fp16.safetensors":
        "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors",
    "models/vae/ae.safetensors":
        "https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors",

    "models/loras/aidmaNSFWunlock-FLUX-V0.2.safetensors":
        "https://drive.google.com/uc?id=1jdc7Qz7BMRqtTkdt49RWwqvHCc3qKo0c",
}

# 確実にディレクトリ作成
for rel_path in files.keys():
    dir_path = os.path.join(BASE_DIR, os.path.dirname(rel_path))
    os.makedirs(dir_path, exist_ok=True)

def download_file(url, dest):
    """Hugging Face ファイルをダウンロードして保存"""
    response = requests.get(url, headers=HEADERS, stream=True)
    response.raise_for_status()
    total = int(response.headers.get("content-length", 0))
    with open(dest, "wb") as f, tqdm(
        desc=os.path.basename(dest),
        total=total,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # keep-alive対策
                size = f.write(chunk)
                bar.update(size)

# ダウンロード実行
for rel_path, url in files.items():
    dest_path = os.path.join(BASE_DIR, rel_path)
    if not os.path.exists(dest_path):
        print(f"⬇️ Downloading: {os.path.basename(dest_path)}")
        download_file(url, dest_path)
    else:
        print(f"✅ Already exists: {os.path.basename(dest_path)}")

print("\n🎉 All model files are ready!")
