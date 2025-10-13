import gdown

# WAN General NSFW model (NSFW-22-H-e8)
url = "https://drive.google.com/uc?id=1oCpmSoG8fcOaZ7iaSyl0eSw8JneOo5DO"
output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_nsfw_high.safetensors"
gdown.download(url, output, quiet=False)

# WAN General NSFW model (NSFW-22-L-e8)
url = "https://drive.google.com/uc?id=1NCYbONFzYvWHSjpWzYGZDUeUkD3-WbjO"
output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_nsfw_low.safetensors"
gdown.download(url, output, quiet=False)

# Pov Missionary High
# url = "https://drive.google.com/uc?id=1AGtKAFoDmnz0huXuDqOqxXzASfsSSiUg"
# output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_pov_high.safetensors"
# gdown.download(url, output, quiet=False)

# Pov Missionary Loe
# url = "https://drive.google.com/uc?id=1-2Dt-EcJvZ1-0SXV3AYXqIjLAWl6oMRQ"
# output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_pov_low.safetensors"
# gdown.download(url, output, quiet=False)
