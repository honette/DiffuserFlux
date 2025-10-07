import os
os.environ["HF_HOME"] = "/workspace/hf_cache"
os.environ["HF_HUB_CACHE"] = "/workspace/hf_cache"

from datetime import datetime
import readline
from huggingface_hub import login
from diffusers import QwenImageEditPlusPipeline
import torch
from PIL import Image

login(token=os.environ["HF_TOKEN"])

pipe = QwenImageEditPlusPipeline.from_pretrained(
    "Qwen/Qwen-Image-Edit-2509",
    torch_dtype=torch.bfloat16,
    cache_dir="/workspace/hf_cache",
    low_cpu_mem_usage=True
).to("cuda")

pipe.set_progress_bar_config(disable=None)
image1 = Image.open("sample/person.png")
image2 = Image.open("sample/dog.png")

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
    filename = f"qwen_img2img_{timestamp}.png"
    save_path = os.path.join(output_dir, filename)
    image.save(save_path)
    print(f"Completed : {filename}")
