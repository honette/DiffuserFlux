#!/usr/bin/env python3
import os, json, requests, time, argparse, datetime
from PIL import Image
import uuid

# ==== 設定 ====
WORKFLOW_PATH = "/workspace/runpod-slim/ComfyUI/api-video_wan2_2_14B_i2v.json"
IMAGE_DIR = "/workspace/runpod-slim/ComfyUI/input_images"
API_URL = "http://127.0.0.1:8188/prompt"
LOG_DIR = "/workspace/runpod-slim/ComfyUI/logs"

POS_PROMPT = "Description: As soon as the video begins, The girls's all worn items fly off in an instant, The girls are completely naked including the lower body, also nipples and pussy, Then The girls jumps little by little; Constraints: head orientation remains constant throughout the motion; Camera: fixed front, The composition does not change; Mood: She is teenager, She has large nipples;"
NEG_PROMPT = "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走"

# ==== 引数 ====
parser = argparse.ArgumentParser(description="Batch image-to-video queue script (with resume) for Wan2.2 on RunPod")
parser.add_argument("--limit", type=int, default=None, help="最大処理数")
parser.add_argument("--skip", type=int, default=0, help="先頭からスキップする件数")
parser.add_argument("--resume", action="store_true", help="最新のログから未処理ファイルをスキップ")
args = parser.parse_args()

# ==== ログ準備 ====
os.makedirs(LOG_DIR, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
log_path = os.path.join(LOG_DIR, f"batch_i2v_{timestamp}.log")

def log(msg):
    """print + ファイル出力"""
    print(msg)
    with open(log_path, "a") as f:
        f.write(msg + "\n")

log(f"🕓 Start: {timestamp}")
log(f"Args: skip={args.skip}, limit={args.limit}, resume={args.resume}")

# ==== ワークフロー読み込み ====
with open(WORKFLOW_PATH) as f:
    workflow = json.load(f)

# ==== ノードIDを直接指定（fp8_scaled 4Steps系統 / mode=4）====
load_id = 97      # LoadImage
pos_id = 93       # Positive CLIPTextEncode
neg_id = 89       # Negative CLIPTextEncode
save_id = 108      # SaveVideo
video_node_id = 98 # WanImageToVideo

log(f"Detected nodes → LoadImage:{load_id}, Positive:{pos_id}, Negative:{neg_id}, SaveVideo:{save_id}")

if 'video_node_id' in locals():
    log(f"Detected video node for resizing: {video_node_id}")

# 追加：配線検証
def ensure_link(from_node, to_node, links):
    for L in links:
        # L = [link_id, from_node, from_slot, to_node, to_slot, "TYPE"]
        if len(L) >= 6 and L[1] == from_node and L[3] == to_node:
            return True
    return False

# ==== 入力画像 ====
images = sorted([
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])
if not images:
    log("❌ No images found in input_images/")
    raise SystemExit(1)

# ==== resume機能 ====
processed = set()
if args.resume:
    logs = sorted([f for f in os.listdir(LOG_DIR) if f.startswith("batch_i2v_")])
    if logs:
        last_log = os.path.join(LOG_DIR, logs[-1])
        log(f"🔄 Resume mode: checking {last_log}")
        with open(last_log, "r") as f:
            for line in f:
                if "→" in line and "▶" in line:
                    parts = line.strip().split("→")
                    if len(parts) == 2:
                        processed_file = parts[1].split(".")[0].strip()  # i2v_xxx
                        processed.add(processed_file)
        log(f"Found {len(processed)} processed entries in last log.")
    else:
        log("⚠️ No previous log found, starting fresh.")

# ==== skip/limit適用 ====
images = images[args.skip : (args.skip + args.limit) if args.limit else None]
total = len(images)
log(f"Processing {total} image(s): {images[0]} ... {images[-1]}")

# ==== メインループ ====
for i, img in enumerate(images, start=1):
    basename, _ = os.path.splitext(img)
    out_name = f"i2v_{basename}"
    if args.resume and out_name in processed:
        log(f"[{i}/{total}] ⏩ Skipped (already processed): {img}")
        continue

    img_path = f"input_images/{img}"
    log(f"[{i}/{total}] ▶ {img_path} → {out_name}.mp4")

    # === 画像の縦横判定して出力サイズ変更 ===
    try:
        with Image.open(os.path.join(IMAGE_DIR, img)) as im:
            w, h = im.size
        ratio = w / h

        if 0.9 <= ratio <= 1.1:
            # ほぼ正方形
            width, height = 640, 640
            log(f"   ↳ square {w}x{h} → 640x640")
        elif h > w:
            # 縦長
            width, height = 512, 768
            log(f"   ↳ portrait {w}x{h} → 512x768")
        else:
            # 横長
            width, height = 768, 512
            log(f"   ↳ landscape {w}x{h} → 768x512")

        # WanImageToVideo ノードに設定
        workflow[str(video_node_id)]["inputs"]["width"] = width
        workflow[str(video_node_id)]["inputs"]["height"] = height

    except Exception as e:
        log(f"   ⚠️ Could not adjust resolution for {img}: {e}")

    # === ノードごとの入力設定 ===
    IMAGE_DIR = "/workspace/runpod-slim/ComfyUI/input_images"
    workflow[str(load_id)]["inputs"]["image"] = os.path.join(IMAGE_DIR, img)
    workflow[str(pos_id)]["inputs"]["text"] = POS_PROMPT
    workflow[str(neg_id)]["inputs"]["text"] = NEG_PROMPT
    workflow[str(save_id)]["inputs"]["filename_prefix"] = f"video/i2v_{basename}"
    workflow[str(save_id)]["inputs"]["format"] = "mp4"

    try:
        payload = {"prompt": workflow, "client_id": str(uuid.uuid4())}
        r = requests.post(API_URL, json=payload)
        if r.ok:
            log(f"  ✅ Queued successfully ({i}/{total})")
        else:
            log(f"  ⚠️ Failed ({i}/{total}): {r.status_code} {r.text}")
    except Exception as e:
        log(f"  ❌ Error ({i}/{total}): {e}")

    time.sleep(1)

log("🏁 Done.")
log(f"Log saved to: {log_path}")
