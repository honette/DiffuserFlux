# 🚀 RunPod 上で Flux1.Kontact + Diffusers 環境構築手順

- GPUメモリ48GB以上のPodを選択
- Podテンプレートは `Runpod Pytorch 2.8.0`
- Expose HTTP Portsに8188を追加 `8188,8888` (ComfyUI用)

- 秘密鍵はWSL上の `~/.ssh/id_runpod` に保存してパーミッション `600` にする
- SSH接続、SCPダウンロード (アドレスは適宜変更）

```bash
ssh root@69.30.85.30 -p 22044 -i ~/.ssh/id_runpod
rsync -avz -e "ssh -i ~/.ssh/id_runpod -p 22044" root@69.30.85.30:/workspace/DiffuserFlux/tmp/ ./
rsync -avz -e "ssh -i ~/.ssh/id_runpod -p 22044" root@69.30.85.30:/workspace/DiffuserFlux/batch/outputs/ ./
```

## 1. 作業環境構築

```bash
apt update; apt install -y vim
cd /workspace
git clone https://github.com/honette/DiffuserFlux.git
cd DiffuserFlux/
pip install -r requirements.txt
```

- **HF_TOKENをexportする**

```
# venv環境にライブラリをインストールする場合は `pip install` せず
bash setup.sh
```

- Flux Kontextを起動する

```
python download_lora_flux.py
python unzip_images.py
python flux_img2img.py --image batch/source_images/hashimoto-kanna_010.jpg
```

- Wan2.2を起動する

```
python unzip_images.py
python wan_i2v_console.py

# 対話で画像を渡す
> load: batch/source_images/hashimoto-kanna_010.jpg
```

## 開発状況

- 動作検証済みは flux_img2img.py のみ

## 画像素材・LoRAについて

- NSFW対応LoRAはGoogle Driveからダウンロード `download_lora.py`
- バッチ実行用のサンプル画像もGoogle Driveからダウンロード `unzip_images.py`

## トラブルシューティング

```
# ターミナルがフリーズ、プロセスだけが残った
ps aux | grep python
kill 1234

```

---

## Flux-Kontext Sample Prompt

何を維持して、何を変更するのかを明確にするのがポイント

- 正方形に自動整形
  - extend the canvas with seamless outpainting to create a square format while preserving the original style and lighting.
- モデルも構図もそのまま、服装とポーズの変更
  - The woman playing at beach. Change her outfit to a bikini swimsuit. she posing excited her both arms up.
  - Change the woman's current clothing to a camisole instead. Adjust her pose so that her arm and hand are relaxed by her side, removing the pointing gesture.
- モデルだけそのまま、元の構図を無視させる
  - This female model is in a completely different cinematic scene. Change to a stylish pose like in a fashion magazine. Change her outfit to a bikini swimsuit.
- NSFW
  - Change the woman's current clothing to take her clothes off completely, Adjust her pose so that her arm and hand are relaxed by her side, removing the gesture. nsfw, nude, And modify her body to a natural and healthy anatomical shape
  - Change the woman's pose to undressing shirt to take her clothes off and showing her breasts, nsfw, nude
- 完成版
  - Extend the canvas with seamless outpainting to create a square format while preserving the original style and lighting, Change the woman's current clothing to take her clothes off completely, Adjust her pose so that her arm and hand are relaxed by her side, removing the gesture. nsfw, nude, And modify her body to a natural and healthy anatomical shape

---

## バッチ実行

### ファイル構造

```
/batch
 ├─ common_prompt.txt        ← 全体に共通で使うプロンプト
 ├─ /source_images           ← 元画像（img2img入力）
 │   ├─ image01.jpg
 │   ├─ image02.jpg
 │   └─ ...
 └─ /outputs                 ← 出力先（自動生成）
     ├─ image01_20251008.jpg
     ├─ image02_20251008.jpg
     └─ ...
```

- 対応している画像拡張子 (PILが開ける奴)

```
supported_ext = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp", "*.tiff", "*.tif")
```

---

## Wan2.2 5B Prompt Testing

- Description: She quickly strips off her clothes, becomes completely naked, and bends forward; Camera Position: Fixed in front; Mood: Quiet photo session
- Description: She slowly puts on a jacket and adjusts the collar; Camera: fixed front, medium shot, keep full body in frame; Mood: calm indoor photo session, Lighting: soft daylight studio
- Description: Her clothes fall apart, becomes completely naked; Constraints: Keeps her head orientation unchanged; Camera Position: Fixed in front; Mood: Quiet photo session
- Description: Her clothes fall apart, becomes weared only bikini swimwear; Constraints: Keeps her head orientation unchanged; Camera Position: Fixed in front; Mood: Quiet photo session

---

## **Flux Kontext Prompt Techniques**

### **1. Basic Modifications**

- Simple and direct: **`"Change the car color to red"`**
- Maintain style: **`"Change to daytime while maintaining the same style of the painting"`**

### **2. Style Transfer**

**Principles:**

- Clearly name style: **`"Transform to Bauhaus art style"`**
- Describe characteristics: **`"Transform to oil painting with visible brushstrokes, thick paint texture"`**
- Preserve composition: **`"Change to Bauhaus style while maintaining the original composition"`**

### **3. Character Consistency**

**Framework:**

- Specific description: **`"The woman with short black hair"`** instead of “she”
- Preserve features: **`"while maintaining the same facial features, hairstyle, and expression"`**
- Step-by-step modifications: Change background first, then actions

### **4. Text Editing**

- Use quotes: **`"Replace 'joy' with 'BFL'"`**
- Maintain format: **`"Replace text while maintaining the same font style"`**

## **Common Problem Solutions**

### **Character Changes Too Much**

❌ Wrong:

```
"Transform the person into a Viking"
```

✅ Correct:

```
"Change the clothes to be a viking warrior while preserving facial features"
```

### **Composition Position Changes**

❌ Wrong:

```
"Put him on a beach"
```

✅ Correct:

```
"Change the background to a beach while keeping the person in the exact same position, scale, and pose"
```

### **Style Application Inaccuracy**

❌ Wrong:

```
"Make it a sketch"
```

✅ Correct:

```
"Convert to pencil sketch with natural graphite lines, cross-hatching, and visible paper texture"
```
