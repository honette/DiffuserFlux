import os

# === Hugging Face キャッシュ設定 ===
os.environ["HF_HOME"] = "/workspace/hf_cache"
os.environ["HF_HUB_CACHE"] = "/workspace/hf_cache"

import argparse
import readline
from datetime import datetime
from huggingface_hub import login
from diffusers import FluxKontextPipeline
from PIL import Image
import piexif
import torch

# === 引数定義 ===
parser = argparse.ArgumentParser()
parser.add_argument("--image", help="Initial image path for img2img mode")
args = parser.parse_args()

# === LoRA設定 ===
lora_uncensored = "/workspace/DiffuserFlux/lora_flux_uncensored.safetensors"
lora_nsfw = "/workspace/DiffuserFlux/lora_flux_nsfw.safetensors"

use_lora = os.path.exists(lora_uncensored) and os.path.exists(lora_nsfw)

if not use_lora:
    print("⚠️  One or more LoRA files missing.")
    ans = input("Continue without LoRA? [y/N]: ").strip().lower()
    if ans != "y":
        print("Aborted.")
        exit()

# === 認証 ===
login(token=os.environ["HF_TOKEN"])

# === モデルロード ===
pipe = FluxKontextPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    torch_dtype=torch.bfloat16,
    cache_dir="/workspace/hf_cache",
    low_cpu_mem_usage=True
).to("cuda")

if use_lora:
    pipe.load_lora_weights(lora_uncensored, adapter_name="uncensored")
    pipe.load_lora_weights(lora_nsfw, adapter_name="nsfw")
    pipe.set_adapters(["uncensored", "nsfw"], adapter_weights=[0.8, 0.8])
    print("✅ LoRA loaded successfully.")

# === 画像モード設定 ===
current_image = None
if args.image:
    if os.path.exists(args.image):
        current_image = Image.open(args.image).convert("RGB")
        print(f"📷 Loaded initial image: {args.image}")
    else:
        print(f"⚠️  Initial image not found: {args.image}")
        exit()
else:
    ans = input("No image specified. Start in txt2img mode? [y/N]: ").strip().lower()
    if ans != "y":
        print("Aborted.")
        exit()
    print("📝 Starting in txt2img mode (no input image).")

# === 操作ガイド ===
print("""
🧠  Flux Interactive Console
---------------------------------------
Commands:
  load: <filename>   → 画像を切り替え（img2imgモード）
  exit               → 終了
  (テキスト入力)     → プロンプトとして生成実行
---------------------------------------
""")

# === 対話ループ ===
while True:
    prompt = input("\nType prompt (or command): ").strip()

    if prompt.lower() == "exit":
        print("👋 Bye!")
        break

    elif prompt.lower().startswith("load:"):
        path = prompt.split("load:", 1)[1].strip()
        if os.path.exists(path):
            current_image = Image.open(path).convert("RGB")
            print(f"📷 Switched to image: {path}")
        else:
            print(f"⚠️  File not found: {path}")
        continue

    # --- 生成開始 ---
    if current_image is not None:
        print(f"Now generating (img2img) → {prompt}")
        result = pipe(image=current_image, prompt=prompt, guidance_scale=2.5).images[0]
    else:
        print(f"Now generating (txt2img) → {prompt}")
        result = pipe(prompt=prompt, guidance_scale=2.5).images[0]

    # === 保存処理 ===
    output_dir = "./tmp"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"flux_output_{timestamp}.jpg"
    save_path = os.path.join(output_dir, filename)

    # Exifにプロンプトを埋め込む
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = prompt.encode("utf-8")
    exif_bytes = piexif.dump(exif_dict)

    result.save(save_path, "jpeg", quality=95, exif=exif_bytes)
    print(f"✅ Completed: {save_path}")
