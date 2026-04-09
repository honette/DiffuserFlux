# 起動手順

- **RunPodでComfyUI環境を起動**
    - RTX4090 + ストレージ50GB の Podテンプレートを選択して起動
    - 起動後、ターミナルで /workspace/runpod-slim/ComfyUI/models/checkpoints に移動
- **ワークフローのJSONをダウンロード＆読み込み**
    - Hugging Faceの https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/tree/main からワークフローJSONをダウンロード
    - ComfyUIの画面で **Load**（またはドラッグ＆ドロップ）してワークフローを開く
- **huggingface_hubをインストール + Qwen-Rapid-AIO-v1.safetensors をダウンロード**

```bash
pip install -U huggingface_hub[cli] hf_transfer
hf download Phr00t/Qwen-Image-Edit-Rapid-AIO Qwen-Rapid-AIO-v1.safetensors --local-dir /workspace/runpod-slim/ComfyUI/models/checkpoints/

```

- **ダウンロード完了を確認**（Qwen-Rapid-AIO-v1.safetensors が約29GBで存在することを確認）
- **ComfyUIでモデルを表示＆ロード**
    - ComfyUIブラウザ画面で **Model Library** を開く
    - **Load All Folders** を実行
    - 出てきた **Qwen-Rapid-AIO-v1.safetensors** を **Load Checkpoint** ノードにドラッグ＆ドロップしてロード成功

---

# スクリプトの使い方
- 同フォルダ内のファイルを `/workspace/runpod-slim/ComfyUI/scripts/` に配置
- 実行例

```bash
python3 /workspace/runpod-slim/ComfyUI/scripts/batch_api_qwen-edit.py --limit 20 --skip 0

```
