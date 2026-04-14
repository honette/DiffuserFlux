# 起動手順

- **RunPodでComfyUI環境を起動**
    - RTX4090 + ストレージ50GB の Podテンプレートを選択して起動
    - 起動後、ターミナルで /workspace/runpod-slim/ComfyUI/models/checkpoints に移動
- **ワークフローのJSONをダウンロード＆読み込み**
    - Hugging Faceの https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/tree/main からワークフローJSONをダウンロード
    - ComfyUIの画面で **Load**（またはドラッグ＆ドロップ）してワークフローを開く
- **huggingface_hubをインストール + v19/Qwen-Rapid-AIO-NSFW-v19.safetensors をダウンロード**
    - v19, v19がオススメとのこと

```bash
pip install -U huggingface_hub[cli] hf_transfer
hf download Phr00t/Qwen-Image-Edit-Rapid-AIO v19/Qwen-Rapid-AIO-NSFW-v19.safetensors --local-dir /workspace/runpod-slim/ComfyUI/models/checkpoints/
wget -O /workspace/runpod-slim/ComfyUI/models/loras/snofs.safetensors "https://civitai.com/api/download/models/2474488?token=f9fdfa1a179ff697f808b85f53054b81"

```

- **ダウンロード完了を確認**（Qwen-Rapid-AIO-NSFW-v19.safetensors が約29GBで存在することを確認）
- **ComfyUIでモデルを表示＆ロード**
    - ComfyUIブラウザ画面で **Model Library** を開く
    - **Load All Folders** を実行
    - 出てきた **Qwen-Rapid-AIO-NSFW-v19.safetensors** を **Load Checkpoint** ノードにドラッグ＆ドロップしてロード成功

---

# スクリプトの使い方
- 同フォルダ内のファイルを `/workspace/runpod-slim/ComfyUI/scripts/` に配置
- 実行例

```bash
python3 /workspace/runpod-slim/ComfyUI/scripts/batch_api_qwen-edit.py --limit 20 --skip 0

```

## SNOFS Prompts

Here's a list of some of the terms that work well:
porn cowgirl position with black man
porn cowgirl position with black simple phallic toy
reclining and fingering
squatting, hand in wet white panties
pov, missionary position with black man, vaginal insertion
sheer clothing, translucent breasts
tentacles wrap her whole body, her legs up, vaginal insertion
pulled up tops, bare torso, squatting, spread pussy by hands, vagina gushing
pulled up tops, bare torso, squatting, spread pussy by hands, black plastic toy inserted into vagina
pulled up tops, bare torso, looking camera from back, twisted torso, spread ass by pov hands, opened vagina dripping clear liquid
