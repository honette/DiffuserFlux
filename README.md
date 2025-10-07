# 🚀 RunPod 上で Flux1.Kontact + Diffusers 環境構築手順

- SSH接続、SCPダウンロード (アドレスは適宜変更）

```bash
ssh root@194.68.245.146 -p 22119 -i ~/.ssh/id_runpod
scp -i ~/.ssh/id_runpod -P 22119 -r root@194.68.245.146:/workspace/DiffuserFlux/*.png ./
```

## 1. 作業環境構築

```bash
apt update; apt install -y vim
cd /workspace
git clone https://github.com/honette/DiffuserFlux.git
cd DiffuserFlux/

# venv環境にライブラリをインストール
bash setup.sh

# venvを使わない場合
pip install -r requirements.txt
```

## トラブルシューティング

```
# ターミナルがフリーズ、プロセスだけが残った
ps aux | grep python
kill 1234

```

---

## 2. モデルの配置

* モデルを HuggingFace から `from_pretrained()` で直接落とすか
* ローカルに `flux1-kontact/` ディレクトリを作って配置しておく

例：HuggingFace から直読み

```python
pipe = DiffusionPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    torch_dtype="float16"
).to("cuda")
```

---

## 3. txt2img スクリプト（`txt2img.py`）

```python
import os
os.environ["HF_HOME"] = "/workspace/hf_cache"
os.environ["HF_HUB_CACHE"] = "/workspace/hf_cache"

from huggingface_hub import login
from diffusers import DiffusionPipeline
import torch

login(token=os.environ["HF_TOKEN"])

from diffusers import DiffusionPipeline
import torch
pipe = DiffusionPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    torch_dtype=torch.bfloat16,
    cache_dir="/workspace/hf_cache",
    low_cpu_mem_usage=True
).to("cuda")

prompt = "a futuristic lab with glowing holograms"
image = pipe(prompt=prompt).images[0]
image.save("flux_txt2img.png")
```

---

## 4. img2img スクリプト（`img2img.py`）

```python
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import torch

model_dir = "./models/flux1-kontact"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_dir, torch_dtype=torch.float16
).to("cuda")

init_image = Image.open("input.png").convert("RGB")
prompt = "make this scene look cyberpunk with neon lights"
image = pipe(
    prompt=prompt,
    image=init_image,
    strength=0.7,
    guidance_scale=7.5
).images[0]
image.save("flux_img2img.png")
```

---

## 5. 実行方法

```bash
python txt2img.py
python img2img.py
```

これで **1つのディレクトリ** にモデルを置いて、スクリプトだけ分ければ OK。
Pod が使い捨てなら、毎回 pip install → モデルダウンロード or マウント → スクリプト実行、の流れで安定するよ。

---

👉 質問：ドクターの Flux1.Kontact のモデルファイルって **HuggingFace にある公式版を使う予定**？
それとも **手元で safetensors / ckpt を持ち込み**たい？
