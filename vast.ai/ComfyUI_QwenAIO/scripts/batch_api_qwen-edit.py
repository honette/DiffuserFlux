#!/usr/bin/env python3
import os, json, requests, time, argparse, datetime
from PIL import Image
import uuid

# ==== 設定 ====
IMAGE_DIR = "/workspace/ComfyUI/input_images"
API_URL = "http://127.0.0.1:18188/prompt"
LOG_DIR = "/workspace/ComfyUI/logs"
CONFIG_PATH = "/workspace/ComfyUI/scripts/config_qwen.json"

WORKFLOW_1IMG = "/workspace/ComfyUI/scripts/Qwen-Rapid-AIO_API-v19_1img.json"
WORKFLOW_2IMG = "/workspace/ComfyUI/scripts/Qwen-Rapid-AIO_API-v19_2img.json"

# ==== ログ準備 ====
os.makedirs(LOG_DIR, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
log_path = os.path.join(LOG_DIR, f"batch_qwen_{timestamp}.log")

def log(msg):
    print(msg)
    with open(log_path, "a") as f:
        f.write(msg + "\n")

# ==== コンフィグ読み込み (配列として処理) ====
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as cf:
        config_list = json.load(cf)
    if not isinstance(config_list, list):
        config_list = [config_list] # 単体オブジェクトの場合も配列に変換
else:
    log("❌ Config file not found!")
    raise SystemExit(1)

# ==== ワークフローの事前読み込み ====
with open(WORKFLOW_1IMG) as f:
    wf_1img_base = json.load(f)
with open(WORKFLOW_2IMG) as f:
    wf_2img_base = json.load(f)

# ==== 入力画像リスト ====
images = sorted([
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

# ==== メインループ ====
MAX_SIDE = 1920

for i, img in enumerate(images, start=1):
    img1_full_path = os.path.join(IMAGE_DIR, img)
    basename, ext = os.path.splitext(img)

    # 各画像に対してコンフィグ配列の数だけ実行
    for c_idx, cfg in enumerate(config_list):
        pos_prompt = cfg.get("positive_prompt", "High quality image")
        image2_path = cfg.get("image2_path", None)
        
        # 保存名の設定 (末尾にインデックスを付けて被らないようにする)
        out_name = f"edit/qwen_{basename}_v{c_idx}"

        # ワークフロー選択とベースコピー
        if image2_path:
            workflow = json.loads(json.dumps(wf_2img_base)) # Deep copy
            load_img2_id = "8"
            workflow[load_img2_id]["inputs"]["image"] = image2_path
        else:
            workflow = json.loads(json.dumps(wf_1img_base)) # Deep copy

        # 共通ノードID
        load_img1_id = "7"
        prompt_id    = "3"
        latent_id    = "9"
        save_id      = "10"

        # --- サイズ計算 ---
        try:
            with Image.open(img1_full_path) as im:
                w, h = im.size
            new_w, new_h = (int(w * (MAX_SIDE/max(w,h))), int(h * (MAX_SIDE/max(w,h)))) if max(w,h) > MAX_SIDE else (w,h)
            workflow[latent_id]["inputs"]["width"] = new_w
            workflow[latent_id]["inputs"]["height"] = new_h
        except: pass

        # --- パラメータセット ---
        workflow[load_img1_id]["inputs"]["image"] = os.path.join(IMAGE_DIR, img)
        workflow[prompt_id]["inputs"]["prompt"] = pos_prompt
        workflow[save_id]["inputs"]["filename_prefix"] = out_name

        # --- 送信 ---
        try:
            headers = {
                "Authorization": f"Bearer b2f314b3a2aa19212afbc941b30bf9089fb5b49495e8ad0becd9f2a79042cb64"
                # "Authorization": f"Bearer {OPEN_BUTTON_TOKEN}"
            }
            # client_id をループごとに確実に変える
            cid = str(uuid.uuid4())
            r = requests.post(API_URL, json={"prompt": workflow, "client_id": cid}, headers=headers)
            if r.ok:
                log(f"[{i}/{len(images)}] Queue added: {out_name} ({'2IMG' if image2_path else '1IMG'})")
            else:
                log(f"  ⚠️ API Error: {r.status_code} {r.text}")
        except Exception as e:
            log(f"  ❌ Error: {e}")

    # 次の画像に行く前に少し長めに休む（1.0秒くらい）
    time.sleep(1.0)

log("🏁 Finished adding all batches to queue.")
