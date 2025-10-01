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