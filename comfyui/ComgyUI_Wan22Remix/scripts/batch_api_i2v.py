#!/usr/bin/env python3
import os, json, requests, time, argparse, datetime
from PIL import Image
import uuid

# ==== 設定 ====
IMAGE_DIR = "/workspace/runpod-slim/ComfyUI/input_images"
API_URL = "http://127.0.0.1:8188/prompt"
LOG_DIR = "/workspace/runpod-slim/ComfyUI/logs"
CONFIG_PATH = "/workspace/runpod-slim/ComfyUI/scripts/config_api_i2v.json"

# ==== ログ準備 ====
os.makedirs(LOG_DIR, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
log_path = os.path.join(LOG_DIR, f"batch_i2v_{timestamp}.log")

def log(msg):
    """print + ファイル出力"""
    print(msg)
    with open(log_path, "a") as f:
        f.write(msg + "\n")

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as cf:
        cfg = json.load(cf)
    WORKFLOW_PATH = cfg.get("workflow_path", "/workspace/runpod-slim/ComfyUI/api-video_wan2_2_14B_i2v-with_RIFE.json")
    POS_PROMPT = cfg.get("positive_prompt", "A default positive prompt")
    NEG_PROMPT = cfg.get("negative_prompt", "low quality, blurry, bad anatomy")
    VIDEO_LENGTH = cfg.get("video_length", 81)
else:
    WORKFLOW_PATH = "/workspace/runpod-slim/ComfyUI/api-video_wan2_2_14B_i2v-with_RIFE.json"
    POS_PROMPT = "The girls are punching."
    NEG_PROMPT = "low quality, blurry, bad anatomy"
    VIDEO_LENGTH = 81

log(f"Loaded config from {CONFIG_PATH}")
log(f"  ▶ Positive: {POS_PROMPT[:50]}...")
log(f"  ▶ Negative: {NEG_PROMPT[:50]}...")
log(f"  ▶ Video length: {VIDEO_LENGTH}")

# ==== 引数 ====
parser = argparse.ArgumentParser(description="Batch image-to-video queue script (with resume) for Wan2.2 on RunPod")
parser.add_argument("--limit", type=int, default=None, help="最大処理数")
parser.add_argument("--skip", type=int, default=0, help="先頭からスキップする件数")
parser.add_argument("--resume", action="store_true", help="最新のログから未処理ファイルをスキップ")
args = parser.parse_args()

log(f"🕓 Start: {timestamp}")
log(f"Args: skip={args.skip}, limit={args.limit}, resume={args.resume}")

# ==== ワークフロー読み込み ====
with open(WORKFLOW_PATH) as f:
    workflow = json.load(f)

# ==== ノードIDを直接指定（fp8_scaled 4Steps系統 / mode=4）====
load_id        = 16     # Start Frame LoadImage（widgets_values[0] = filename）
pos_id         = 9      # Positive CLIPTextEncode（widgets_values[0]）
neg_id         = 10     # Negative CLIPTextEncode（widgets_values[0]）
save_id        = 39     # VHS_VideoCombine（widgets_valuesはdict）
video_node_id  = 28     # WanVaceToVideo（widgets_values[0]=width, [1]=height）
length_node_id = 48     # PrimitiveInt（num_frames / VIDEO_LENGTH）

log(f"Detected nodes → LoadImage:{load_id}, Positive:{pos_id}, Negative:{neg_id}, SaveVideo:{save_id}")

if 'video_node_id' in locals():
    log(f"Detected video node for resizing: {video_node_id} (AIO版)")
    log(f"Detected length node: {length_node_id}")

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

        # WanVaceToVideo + PrimitiveInt に設定（AIO版）
        workflow[str(video_node_id)]["widgets_values"][0] = width
        workflow[str(video_node_id)]["widgets_values"][1] = height
        workflow[str(length_node_id)]["widgets_values"][0] = VIDEO_LENGTH
        log(f"   ↳ {w}x{h} → {width}x{height} x {VIDEO_LENGTH} frames (AIO)")

    except Exception as e:
        log(f"   ⚠️ Could not adjust resolution for {img}: {e}")

    # === ノードごとの入力設定 ===
    # Start Frame LoadImage（widgets_values[0] = ファイル名のみ）
    workflow[str(load_id)]["widgets_values"][0] = img

    # Positive / Negative Prompt（widgets_values[0]）
    workflow[str(pos_id)]["widgets_values"][0] = POS_PROMPT
    workflow[str(neg_id)]["widgets_values"][0] = NEG_PROMPT

    # VHS_VideoCombine（widgets_valuesはdict）
    workflow[str(save_id)]["widgets_values"]["filename_prefix"] = f"video/i2v_{basename}"
    # formatはworkflow内で"video/h264-mp4"固定でOK

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
