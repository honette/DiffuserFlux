import os
os.environ["HF_HOME"] = "/workspace/hf_cache"
os.environ["HF_HUB_CACHE"] = "/workspace/hf_cache"

import argparse
import glob
from datetime import datetime
from PIL import Image
import piexif
import torch
from diffusers import FluxKontextPipeline

SUPPORTED_EXT = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp", "*.tiff", "*.tif")

def read_common_prompt(base_dir):
    path = os.path.join(base_dir, "common_prompt.txt")
    sample_path = os.path.join(base_dir, "common_prompt.sample.txt")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
            if prompt:
                print(f"Using common prompt from {path}")
                return prompt
            else:
                print(f"⚠️  Warning: {path} is empty. Trying sample prompt...\n")

    if os.path.exists(sample_path):
        with open(sample_path, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
            if prompt:
                print(f"Using sample prompt from {sample_path}")
                return prompt
            else:
                print(f"⚠️  Warning: {sample_path} is empty as well.")

        raise FileNotFoundError(f"No usable common_prompt.txt or common_prompt.sample.txt found in {base_dir}")
   
def enumerate_source_images(base_dir):
    src_dir = os.path.join(base_dir, "source_images")
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"source_images folder not found in {base_dir}")
    files = []
    for ext in SUPPORTED_EXT:
        files.extend(glob.glob(os.path.join(src_dir, ext)))
    if not files:
        raise FileNotFoundError(f"No source images found in {src_dir}")
    return sorted(files)

def setup_pipeline(use_lora: bool):
    pipe = FluxKontextPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-Kontext-dev",
        torch_dtype=torch.bfloat16,
        cache_dir="/workspace/hf_cache",
        low_cpu_mem_usage=True,
    ).to("cuda")

    lora_path = "/workspace/DiffuserFlux/lora_flux_uncensored.safetensors"
    if use_lora and os.path.exists(lora_path):
        print(f"Loading LoRA: {lora_path}")
        pipe.load_lora_weights(lora_path, adapter_name="uncensored")
        lora_path = "/workspace/DiffuserFlux/lora_flux_nsfw.safetensors"
        pipe.load_lora_weights(lora_path, adapter_name="nsfw")
        pipe.set_adapters(["uncensored", "nsfw"], adapter_weights=[0.8, 0.8])
        print("LoRA loaded.")
    elif use_lora:
        print("LoRA enabled but file not found.")
        return None
    return pipe

def embed_prompt_exif(image: Image.Image, prompt: str, save_path: str):
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = prompt.encode("utf-8")
    exif_bytes = piexif.dump(exif_dict)
    image.save(save_path, "jpeg", quality=95, exif=exif_bytes)

def process_image(pipe, img_path, prompt, base_dir):
    img = Image.open(img_path).convert("RGB")
    result = pipe(image=img, prompt=prompt, guidance_scale=2.5).images[0]

    out_dir = os.path.join(base_dir, "outputs")
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    basename = os.path.splitext(os.path.basename(img_path))[0]
    out_path = os.path.join(out_dir, f"{basename}_{timestamp}.jpg")

    embed_prompt_exif(result, prompt, out_path)
    return out_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        default="/workspace/DiffuserFlux/batch",
        help="Batch directory path (default: /workspace/DiffuserFlux/batch)"
    )
    parser.add_argument("--no-lora", action="store_true", help="Disable LoRA usage")
    args = parser.parse_args()

    prompt = read_common_prompt(args.dir)

    #debug
    print(f"Using prompt: {prompt}")
    if not prompt:
        print("No valid prompt found.")
        return

    pipe = setup_pipeline(use_lora=not args.no_lora)
    if pipe is None:
        print("Pipeline setup failed.")
        return

    images = enumerate_source_images(args.dir)

    for img_path in images:
        print(f"\nProcessing: {img_path}")
        out_path = process_image(pipe, img_path, prompt, args.dir)
        print(f"Completed: {out_path}")

if __name__ == "__main__":
    main()
