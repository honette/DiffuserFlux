#!/usr/bin/env python3
import os, json, requests, time, argparse, datetime
from PIL import Image
import uuid

# ==== 設定 ====
IMAGE_DIR = "/workspace/runpod-slim/ComfyUI/input_images"
API_URL = "http://127.0.0.1:8188/prompt"
LOG_DIR = "/workspace/runpod-slim/ComfyUI/logs"
CONFIG_PATH = "/workspace/runpod-slim/ComfyUI/scripts/config_qwen.json"
WORKFLOW_PATH = "/workspace/runpod-slim/ComfyUI/scripts/Qwen-Rapid-AIO.json"

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
    # 2枚目の画像パスをコンフィグから取得
    IMAGE2_PATH = cfg.get("image2_path", None) 
else:
    POS_PROMPT = "Put the woman holding a balloon next to the ninja in the hallway."
    IMAGE2_PATH = None

log(f"Loaded config from {CONFIG_PATH}")
log(f"  ▶ Positive: {POS_PROMPT[:50]}...")
log(f"  ▶ Image2: {IMAGE2_PATH}")

# ==== ワークフロー読み込み ====
with open(WORKFLOW_PATH) as f:
    workflow = json.load(f)

# ==== ノードID設定 (Qwen-Rapid-AIO.jsonに基づく) ====
load_img1_id = "7"  # メイン画像
load_img2_id = "8"  # 2枚目の画像 (Optional)
prompt_id    = "3"  # TextEncodeQwenImageEditPlus
latent_id    = "9"  # EmptyLatentImage (サイズ変更用)
save_id      = "10" # ※注：PreviewImage(6)をSaveImage(10)に差し替え前提

# ==== 入力画像リスト取得 ====
images = sorted([
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

if not images:
    log("❌ No images found in input_images/")
    raise SystemExit(1)

total = len(images)

# ==== メインループ ====
for i, img in enumerate(images, start=1):
    basename, ext = os.path.splitext(img)
    out_name = f"edit/qwen_{basename}"
    
    img1_path = os.path.join(IMAGE_DIR, img)
    log(f"[{i}/{total}] ▶ {img1_path} → {out_name}{ext}")

    # --- 解像度調整 ---
    try:
        with Image.open(img1_path) as im:
            w, h = im.size
        # そのままのサイズをセット（必要に応じて比率計算を入れる）
        workflow[latent_id]["inputs"]["width"] = w
        workflow[latent_id]["inputs"]["height"] = h
    except Exception as e:
        log(f"   ⚠️ Could not get size: {e}")

    # --- ノード入力設定 ---
    # Image 1 (メイン)
    workflow[load_img1_id]["inputs"]["image"] = img
    
    # Image 2 (コンフィグに指定があれば反映、なければそのまま)
    if IMAGE2_PATH:
        workflow[load_img2_id]["inputs"]["image"] = IMAGE2_PATH

    # Prompt
    workflow[prompt_id]["inputs"]["text"] = POS_PROMPT

    # Output (SaveImageノードを追加・指定する場合)
    # ワークフローにSaveImageノードがない場合は、API経由で一時的に追加するか
    # 既存のノードをSaveImageに書き換える処理が必要です。
    if save_id in workflow:
        workflow[save_id]["inputs"]["filename_prefix"] = out_name

    # --- キュー登録 ---
    try:
        payload = {"prompt": workflow, "client_id": str(uuid.uuid4())}
        r = requests.post(API_URL, json=payload)
        if r.ok:
            log(f"  ✅ Queued: {out_name}")
        else:
            log(f"  ⚠️ Failed: {r.status_code}")
    except Exception as e:
        log(f"  ❌ Error: {e}")

    time.sleep(0.5)

log("🏁 Batch processing complete.")
