import gdown

# WAN General NSFW model (NSFW-22-H-e8)
url = "https://drive.google.com/uc?id=1oCpmSoG8fcOaZ7iaSyl0eSw8JneOo5DO"
output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_nsfw_high.safetensors"
gdown.download(url, output, quiet=False)

# WAN General NSFW model (NSFW-22-L-e8)
url = "https://drive.google.com/uc?id=1NCYbONFzYvWHSjpWzYGZDUeUkD3-WbjO"
output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_nsfw_low.safetensors"
gdown.download(url, output, quiet=False)

# DR34ML4Y_I2V_14B_HIGH
url = "https://drive.google.com/uc?id=1MA_YbTPghda0Np1LKRo3btXpzKx0RtMW"
output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_dr34ml4y_high.safetensors"
gdown.download(url, output, quiet=False)

# DR34ML4Y_I2V_14B_LOW
url = "https://drive.google.com/uc?id=1bQZaHwmz1x7C5HqNh2EPz7C-WXeNd9rp"
output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_dr34ml4y_low.safetensors"
gdown.download(url, output, quiet=False)
