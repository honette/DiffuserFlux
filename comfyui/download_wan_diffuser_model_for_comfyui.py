import os
import requests
from tqdm import tqdm

# 保存先ベースパス
BASE_DIR = "/workspace/runpod-slim/ComfyUI"

# ダウンロード対象ファイル
files = {
    "models/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors":
        # "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors",
        "https://drive.google.com/uc?id=1L7n5Fuhpub12jFWLeuM5Bz6ttP2AAGdf", # for Anime
    "models/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors":
        # "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors",
        "https://drive.google.com/uc?id=1wDVgTRJeAfsIWdgemKT8DmKa2DVJ8xiM", # for Anime
    "models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors":
        "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors",
    "models/vae/wan_2.1_vae.safetensors":
        "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors",
    "models/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors":
        "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors",
    "models/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors":
        "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors",
}

# 確実にディレクトリ作成
for rel_path in files.keys():
    dir_path = os.path.join(BASE_DIR, os.path.dirname(rel_path))
    os.makedirs(dir_path, exist_ok=True)

def download_file(url, dest):
    """Hugging Face ファイルをダウンロードして保存"""
    response = requests.get(url, stream=True)
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
