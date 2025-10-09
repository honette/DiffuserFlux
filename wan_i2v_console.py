import os
import torch
import numpy as np
from datetime import datetime
from diffusers import WanImageToVideoPipeline
from diffusers.utils import export_to_video, load_image

# === Hugging Face キャッシュ設定 ===
os.environ["HF_HOME"] = "/workspace/hf_cache"
os.environ["HF_HUB_CACHE"] = "/workspace/hf_cache"

# === 定数 ===
MODEL_ID = "Wan-AI/Wan2.2-TI2V-5B-Diffusers"
DEVICE = "cuda"
DTYPE = torch.bfloat16

# === 認証 ===
from huggingface_hub import login
login(token=os.environ.get("HF_TOKEN", ""))

# === モデルロード ===
print("🚀 Loading Wan2.2 pipeline... (this may take a while)")
pipe = WanImageToVideoPipeline.from_pretrained(MODEL_ID, torch_dtype=DTYPE)
pipe.to(DEVICE)
print("✅ Model loaded successfully.")

# === LoRA関連 (将来対応用) ===
"""
lora_uncensored = "/workspace/DiffuserFlux/lora_flux_uncensored.safetensors"
lora_nsfw = "/workspace/DiffuserFlux/lora_flux_nsfw.safetensors"
if os.path.exists(lora_uncensored) and os.path.exists(lora_nsfw):
    pipe.load_lora_weights(lora_uncensored, adapter_name="uncensored")
    pipe.load_lora_weights(lora_nsfw, adapter_name="nsfw")
    pipe.set_adapters(["uncensored", "nsfw"], adapter_weights=[0.8, 0.8])
    print("✅ LoRA loaded successfully.")
else:
    print("⚠️  LoRA files missing. Skipping.")
"""

# === 画像の初期設定 ===
current_image = None

print("""
🧠  Wan2.2 Interactive Console
---------------------------------------
Commands:
  load: <filename>   → 入力画像を切り替え
  exit               → 終了
  (テキスト入力)     → プロンプトとして生成実行
---------------------------------------
""")

while True:
    prompt = input("\nType prompt (or command): ").strip()

    if prompt.lower() == "exit":
        print("👋 Bye!")
        break

    elif prompt.lower().startswith("load:"):
        path = prompt.split("load:", 1)[1].strip()
        if os.path.exists(path):
            current_image = load_image(path)
            print(f"📷 Loaded image: {path}")
        else:
            print(f"⚠️  File not found: {path}")
        continue

    if current_image is None:
        print("⚠️  No image loaded. Use 'load: <path>' first.")
        continue

    try:
        num_frames_input = input("Number of frames [default=81]: ").strip()
        num_frames = int(num_frames_input) if num_frames_input else 81
    except ValueError:
        num_frames = 81

    # === 解像度自動調整 ===
    max_area = 480 * 832
    aspect_ratio = current_image.height / current_image.width
    mod_value = pipe.vae_scale_factor_spatial * pipe.transformer.config.patch_size[1]
    height = round(np.sqrt(max_area * aspect_ratio)) // mod_value * mod_value
    width = round(np.sqrt(max_area / aspect_ratio)) // mod_value * mod_value
    resized = current_image.resize((width, height))

    # === 生成 ===
    print(f"🎬 Generating video... ({num_frames} frames)")
    generator = torch.Generator(device=DEVICE).manual_seed(0)

    output_frames = pipe(
        image=resized,
        prompt=prompt,
        negative_prompt="色调艳丽,过曝,静态,细节模糊不清,字幕,风格,作品,画作,画面,静止,整体发灰,最差质量,低质量,JPEG压缩残留,丑陋的,残缺的,多余的手指,画得不好的手部,画得不好的脸部,畸形的,毁容的,形态畸形的肢体,手指融合,静止不动的画面,杂乱的背景,三条腿,背景人很多,倒着走",
        height=height,
        width=width,
        num_frames=num_frames,
        guidance_scale=3.5,
        num_inference_steps=40,
        generator=generator,
    ).frames[0]

    # === 保存 ===
    output_dir = "./tmp"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"wan_output_{timestamp}.mp4"
    save_path = os.path.join(output_dir, filename)

    export_to_video(output_frames, save_path, fps=16)
    print(f"✅ Completed: {save_path}")
