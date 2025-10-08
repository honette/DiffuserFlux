import os
os.environ["HF_HOME"] = "/workspace/hf_cache"
os.environ["HF_HUB_CACHE"] = "/workspace/hf_cache"

lora_path = "/workspace/DiffuserFlux/lora_flux_uncensored.safetensors"
use_lora = False
if os.path.exists(lora_path):
    print(f"Found LoRA file: {lora_path}")
    use_lora = True
else:
    ans = input("⚠️ LoRA file not found. Continue without LoRA? [y/N]: ").strip().lower()
    if ans != "y":
        print("Aborted.")
        exit()

from datetime import datetime
import readline
from huggingface_hub import login
from diffusers import FluxKontextPipeline
from diffusers.utils import load_image
from PIL import Image, ExifTags
import torch

login(token=os.environ["HF_TOKEN"])

pipe = FluxKontextPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    torch_dtype=torch.bfloat16,
    cache_dir="/workspace/hf_cache",
    low_cpu_mem_usage=True
).to("cuda")

if use_lora:
    pipe.load_lora_weights(
        "/workspace/DiffuserFlux/lora_flux_uncensored.safetensors",
        adapter_name="uncensored"
    )
    pipe.load_lora_weights(
        "/workspace/DiffuserFlux/lora_flux_nsfw.safetensors",
        adapter_name="nsfw"
    )
    pipe.set_adapters(["uncensored", "nsfw"], adapter_weights=[0.8, 0.8])

    print("✅ LoRA loaded successfully.")

input_image = Image.open("sample/person.jpg")

while True:
    prompt = input("\nType prompts : ")
    if prompt.strip().lower() == "exit":
        print("Bye!")
        break

    print(f"Now Generating : {prompt}")
    image = pipe(
        image=input_image,
        prompt=prompt,
        guidance_scale=2.5
    ).images[0]

    output_dir = "./tmp"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"flux_img2img_{timestamp}.jpg"
    save_path = os.path.join(output_dir, filename)

    # ExifにUserCommentとしてプロンプトを格納
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = prompt.encode("utf-8")
    exif_bytes = piexif.dump(exif_dict)

    image.save(save_path, "jpeg", quality=95, exif=exif_bytes)

    print(f"Completed : {save_path}")
