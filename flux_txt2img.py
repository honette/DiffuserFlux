import os
os.environ["HF_HOME"] = "/workspace/hf_cache"
os.environ["HF_HUB_CACHE"] = "/workspace/hf_cache"

lora_path = "/workspace/DiffuserFlux/lora_model.safetensors"
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
from diffusers import DiffusionPipeline
import torch

login(token=os.environ["HF_TOKEN"])

pipe = DiffusionPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    torch_dtype=torch.bfloat16,
    cache_dir="/workspace/hf_cache",
    low_cpu_mem_usage=True
).to("cuda")

if use_lora:
    pipe.load_lora_weights(lora_path)
    print("✅ LoRA loaded successfully.")

while True:
    prompt = input("\nType prompts : ")
    if prompt.strip().lower() == "exit":
        print("Bye!")
        break

    print(f"Now Generating : {prompt}")
    image = pipe(prompt=prompt).images[0]

    output_dir = "./tmp"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"flux_txt2img_{timestamp}.jpg"
    save_path = os.path.join(output_dir, filename)
    image.save(save_path, format="JPEG", quality=95)

    print(f"Completed : {save_path}")
