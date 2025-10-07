import os
os.environ["HF_HOME"] = "/workspace/hf_cache"
os.environ["HF_HUB_CACHE"] = "/workspace/hf_cache"

from datetime import datetime
import readline
from huggingface_hub import login
from diffusers import FluxKontextPipeline
from diffusers.utils import load_image
from PIL import Image
import torch

login(token=os.environ["HF_TOKEN"])

pipe = FluxKontextPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    torch_dtype=torch.bfloat16,
    cache_dir="/workspace/hf_cache",
    low_cpu_mem_usage=True
).to("cuda")

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

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"flux_img2img_{timestamp}.png"
    save_path = os.path.join(output_dir, filename)
    image.save(save_path)
    print(f"Completed : {filename}")
