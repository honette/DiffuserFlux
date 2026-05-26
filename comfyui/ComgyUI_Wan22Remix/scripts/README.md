# 起動手順

- **RunPodでComfyUI環境を起動**
    - RTX4090 + ストレージ50GB の Podテンプレートを選択して起動
    - 起動後、ターミナルで /workspace/runpod-slim/ComfyUI/models/checkpoints に移動

```bash
pip install -U huggingface_hub[cli] hf_transfer
hf download FX-FeiHou/wan2.2-Remix NSFW/Wan2.2_Remix_NSFW_i2v_14b_high_lighting_fp8_e4m3fn_v3.0.safetensors --local-dir /workspace/runpod-slim/ComfyUI/models/diffusion_models/
hf download FX-FeiHou/wan2.2-Remix NSFW/Wan2.2_Remix_NSFW_i2v_14b_low_lighting_fp8_e4m3fn_v3.0.safetensors --local-dir /workspace/runpod-slim/ComfyUI/models/diffusion_models/
hf download NSFW-API/NSFW-Wan-UMT5-XXL nsfw_wan_umt5-xxl_fp8_scaled.safetensors --local-dir /workspace/runpod-slim/ComfyUI/models/text_encoders/
hf download Comfy-Org/Wan_2.2_ComfyUI_Repackaged split_files/vae/wan_2.1_vae.safetensors --local-dir /workspace/runpod-slim/ComfyUI/models/vae/
hf download Kijai/WanVideo_comfy LoRAs/Wan22-Lightning/old/Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH_fp16.safetensors --local-dir /workspace/runpod-slim/ComfyUI/models/loras/
hf download Kijai/WanVideo_comfy LoRAs/Wan22-Lightning/old/Wan2.2-Lightning_I2V-A14B-4steps-lora_LOW_fp16.safetensors --local-dir /workspace/runpod-slim/ComfyUI/models/loras/
wget -O /workspace/runpod-slim/ComfyUI/models/loras/BoobSizeSlider-High.safetensors "https://civitai.com/api/download/models/2665828?token=f9fdfa1a179ff697f808b85f53054b81"
wget -O /workspace/runpod-slim/ComfyUI/models/loras/BoobSizeSlider-Low.safetensors "https://civitai.com/api/download/models/2665880?token=f9fdfa1a179ff697f808b85f53054b81"

```

CIVITAI API KEY forcomfy
f9fdfa1a179ff697f808b85f53054b81

---

# スクリプトの使い方
- scripts, input_imagesフォルダをPod上のComfyUIディレクトリにコピーする
- 実行例

```bash
python3 /workspace/runpod-slim/ComfyUI/scripts/batch_api_qwen-edit.py

```

---
## Sample Prompts

```
4k high resolution, Fast forward video. 4x speed movements.high speed action. she is young teenager, lolita. camera pull back to reveal her full body. Camera dollies out, (((Extremely skinny))). (((((extremely small breasts))))).

hentai animation. japanese hentai porn. she undress and rip outfits, she throw out own outfits. she is topless, slender naked body, breasts and nipples, expose vagina.
she squat up and down, bounce hip up and down, suppoert breasts on arms, vaginai insertion with black dildo grown ground. hopping. extremely excited sex.
```
