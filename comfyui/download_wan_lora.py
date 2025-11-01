import gdown

# DR34ML4Y_I2V_14B_HIGH
url = "https://drive.google.com/uc?id=1MA_YbTPghda0Np1LKRo3btXpzKx0RtMW"
output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_dr34ml4y_high.safetensors"
gdown.download(url, output, quiet=False)

# DR34ML4Y_I2V_14B_LOW
url = "https://drive.google.com/uc?id=1bQZaHwmz1x7C5HqNh2EPz7C-WXeNd9rp"
output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_dr34ml4y_low.safetensors"
gdown.download(url, output, quiet=False)

# Breasts Physics wan22-m4crom4sti4-i2v-high-k3nk
url = "https://drive.google.com/uc?id=1wG2QBNr5e44XyfhOyCgrgBG9OLUhdZJG"
output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_physics_high.safetensors"
gdown.download(url, output, quiet=False)

# Breasts Physics wan22-m4crom4sti4-i2v-low-k3nk
url = "https://drive.google.com/uc?id=12fV7JMh4p4WyZTZcso2q7pKeEDowlqhs"
output = "/workspace/runpod-slim/ComfyUI/models/loras/lora_wan_physics_low.safetensors"
gdown.download(url, output, quiet=False)
