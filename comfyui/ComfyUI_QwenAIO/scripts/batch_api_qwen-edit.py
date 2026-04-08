#!/usr/bin/env python3
import os, json, requests, time, argparse, datetime
from PIL import Image
import uuid

# ==== 設定 ====
IMAGE_DIR = "/workspace/runpod-slim/ComfyUI/input_images"
API_URL = "http://127.0.0.1:8188/prompt"
LOG_DIR = "/workspace/runpod-slim/ComfyUI/logs"
CONFIG_PATH = "/workspace/runpod-slim/ComfyUI/scripts/config_qwen.json"
WORKFLOW_PATH = "/workspace/runpod-slim/ComfyUI/scripts/Qwen-Rapid-AIO_API.json"

# ==== ログ準備 ====
os.makedirs(LOG_DIR, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
log_path = os.path.join(LOG_DIR, f"batch_qwen_{timestamp}.log")

def log(msg):
    print(msg)
    with open(log_path, "a") as f:
        f.write(msg + "\n")

# ==== コンフィグ読み込み ====
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as cf:
        cfg = json.load(cf)
    POS_PROMPT = cfg.get("positive_prompt", "High quality image")
    IMAGE2_PATH = cfg.get("image2_path", None) 
else:
    POS_PROMPT = "High quality image"
    IMAGE2_PATH = None

log(f"Loaded config from {CONFIG_PATH}")
log(f"  ▶ Positive: {POS_PROMPT[:50]}...")

# ==== ワークフロー読み込み ====
with open(WORKFLOW_PATH) as f:
    workflow = json.load(f)

# ==== ノードID設定 (Qwen-Rapid-AIO_API.json準拠) ====
# ニシが直す予定の「image1/image2」構成を前提にしておくね！
load_img1_id = "7"  # メイン画像 (後で直す用)
load_img2_id = "8"  # 2枚目画像
prompt_id    = "3"  # TextEncodeQwenImageEditPlus
latent_id    = "9"  # EmptyLatentImage
save_id      = "10" # SaveImage

# ==== 入力画像リスト ====
images = sorted([
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

if not images:
    log("❌ No images found in input_images/")
    raise SystemExit(1)

# ==== メインループ ====
MAX_SIDE = 1920

for i, img in enumerate(images, start=1):
    basename, ext = os.path.splitext(img)
    out_name = f"edit/qwen_{basename}"
    img1_full_path = os.path.join(IMAGE_DIR, img)
    
    log(f"[{i}/{len(images)}] ▶ {img} → {out_name}")

    # --- 解像度計算 (長辺MAX 1920) ---
    try:
        with Image.open(img1_full_path) as im:
            w, h = im.size
        
        if max(w, h) > MAX_SIDE:
            scale = MAX_SIDE / max(w, h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            log(f"   ↳ Scaling: {w}x{h} → {new_w}x{h}")
        else:
            new_w, new_h = w, h
            log(f"   ↳ Size: {w}x{h}")

        workflow[latent_id]["inputs"]["width"] = new_w
        workflow[latent_id]["inputs"]["height"] = new_h
    except Exception as e:
        log(f"   ⚠️ Size Calculation Error: {e}")

    # --- ノード入力設定 ---
    # メイン画像
    workflow[load_img1_id]["inputs"]["image"] = img
    
    # 2枚目画像 (コンフィグにあればセット)
    if IMAGE2_PATH:
        workflow[load_img2_id]["inputs"]["image"] = IMAGE2_PATH

    # プロンプト (API用JSONの項目名 'prompt' に合わせているよ)
    workflow[prompt_id]["inputs"]["prompt"] = POS_PROMPT

    # 出力ファイル名
    workflow[save_id]["inputs"]["filename_prefix"] = out_name

    # --- 送信 ---
    try:
        payload = {"prompt": workflow, "client_id": str(uuid.uuid4())}
        r = requests.post(API_URL, json=payload)
        if r.ok:
            log(f"  ✅ Queued successfully")
        else:
            log(f"  ⚠️ Failed: {r.status_code} - {r.text}")
    except Exception as e:
        log(f"  ❌ Error during request: {e}")

    time.sleep(0.5)

log(f"🏁 Done! Log saved to: {log_path}")