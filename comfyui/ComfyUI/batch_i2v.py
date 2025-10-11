#!/usr/bin/env python3
import os, json, requests, time, argparse, datetime

# ==== 設定 ====
WORKFLOW_PATH = "/workspace/ComfyUI/video_wan2_2_14B_i2v.json"
IMAGE_DIR = "/workspace/ComfyUI/input_images"
API_URL = "http://127.0.0.1:8188/prompt"
LOG_DIR = "/workspace/ComfyUI/logs"

POS_PROMPT = "A cinematic scene of a warrior standing under a glowing moon."
NEG_PROMPT = "low quality, deformed, blurry, bad anatomy"

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

# ==== ノード検出 ====
load_id = pos_id = neg_id = save_id = None
for node in workflow["nodes"]:
    t = node.get("type", "")
    title = node.get("title", "").lower()
    if t == "LoadImage" and load_id is None:
        load_id = node["id"]
    elif "positive" in title:
        pos_id = node["id"]
    elif "negative" in title:
        neg_id = node["id"]
    elif t == "SaveVideo":
        save_id = node["id"]

log(f"Detected nodes → LoadImage:{load_id}, Positive:{pos_id}, Negative:{neg_id}, SaveVideo:{save_id}")

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

    # ノード設定
    if load_id is not None:
        workflow["nodes"][load_id]["widgets_values"][0] = img_path
    if pos_id is not None:
        workflow["nodes"][pos_id]["widgets_values"][0] = POS_PROMPT
    if neg_id is not None:
        workflow["nodes"][neg_id]["widgets_values"][0] = NEG_PROMPT
    if save_id is not None:
        workflow["nodes"][save_id]["widgets_values"][1] = out_name
        workflow["nodes"][save_id]["widgets_values"][2] = "mp4"

    try:
        r = requests.post(API_URL, json=workflow)
        if r.ok:
            log(f"  ✅ Queued successfully ({i}/{total})")
        else:
            log(f"  ⚠️ Failed ({i}/{total}): {r.status_code} {r.text}")
    except Exception as e:
        log(f"  ❌ Error ({i}/{total}): {e}")

    time.sleep(1)

log("🏁 Done.")
log(f"Log saved to: {log_path}")
