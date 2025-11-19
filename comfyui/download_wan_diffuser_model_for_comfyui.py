# filename: download_wan2.2_ultimate_fast_with_token.py
import os
import subprocess
from pathlib import Path

BASE_DIR = Path("/workspace/runpod-slim/ComfyUI")

# 環境変数から自動でトークン取得
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print("⚠️  HF_TOKEN が環境変数に見つからないよ！")
    print("    export HF_TOKEN=hf_XXXXXXXXXXXXXXXX で設定してね")
    exit(1)

# HF_TRANSFER 有効化（これだけで huggingface_hub が爆速Rustになる）
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

MODEL_URLS = {
    "models/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors":
        "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors",
    "models/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors":
        "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors",
    "models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors":
        "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors",
    "models/vae/wan_2.1_vae.safetensors":
        "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors",
    "models/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors":
        "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors",
    "models/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors":
        "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors",
    "models/loras/Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH_fp16.safetensors":
        "https://huggingface.co/Kijai/WanVideo_comfy/blob/main/LoRAs/Wan22-Lightning/old/Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH_fp16.safetensors",
    "models/loras/Wan2.2-Lightning_I2V-A14B-4steps-lora_LOW_fp16.safetensors":
        "https://huggingface.co/Kijai/WanVideo_comfy/blob/main/LoRAs/Wan22-Lightning/old/Wan2.2-Lightning_I2V-A14B-4steps-lora_LOW_fp16.safetensors",
}

def download_ultra_fast(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "aria2c",
        "--console-log-level=warn",
        "--summary-interval=5",
        "--download-result=hide",
        "--max-concurrent-downloads=16",
        "--max-connection-per-server=16",   # HFは16までOK
        "--split=16",
        "--min-split-size=1M",
        "--continue=true",
        "--auto-file-renaming=false",
        "--allow-overwrite=true",
        "--optimize-concurrent-downloads=true",
        "--header=Authorization: Bearer " + HF_TOKEN,   # ← ここで自動認証！
        f"--dir={dest.parent}",
        f"--out={dest.name}",
        url
    ]
    
    print(f"⚡ Start Downloading → {dest.name}")
    subprocess.run(cmd)

# 実行！
for rel_path, url in MODEL_URLS.items():
    dest_path = BASE_DIR / rel_path
    if dest_path.exists():
        print(f"✅ File Already Exists {dest_path.name}")
    else:
        download_ultra_fast(url, dest_path)

print("\nDone!")
