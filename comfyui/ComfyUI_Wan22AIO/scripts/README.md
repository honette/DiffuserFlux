# 起動手順

- **RunPodでComfyUI環境を起動**
    - RTX4090 + ストレージ50GB の Podテンプレートを選択して起動
    - 起動後、ターミナルで /workspace/runpod-slim/ComfyUI/models/checkpoints に移動

```bash
pip install -U huggingface_hub[cli] hf_transfer
hf download Phr00t/WAN2.2-14B-Rapid-AllInOne Mega-v12/wan2.2-rapid-mega-aio-nsfw-v12.2.safetensors --local-dir /workspace/runpod-slim/ComfyUI/models/checkpoints/

```

---

# スクリプトの使い方
- scripts, input_imagesフォルダをPod上のComfyUIディレクトリにコピーする
- 実行例

```bash
python3 /workspace/runpod-slim/ComfyUI/scripts/batch_api_qwen-edit.py

```
