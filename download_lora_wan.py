import gdown

# NSFW-22-H-e8 (NSFW V2.2 Hentai)
url = "https://drive.google.com/uc?id=1-CKoRMcb5tB-K7AfrZg5AGriwAz9fnwC"
output = "/workspace/DiffuserFlux/lora_wan_nsfw.safetensors"
gdown.download(url, output, quiet=False)

# Wan2.2-I2V-A14B-4steps-lora-rank64-Seko-V1_high_noise_model
url = "https://drive.google.com/uc?id=1H1BvxRDtnREO0hOh09nb-iJqYMp2yne_"
output = "/workspace/DiffuserFlux/lora_wan_lightining-high.safetensors"
gdown.download(url, output, quiet=False)

# Wan2.2-I2V-A14B-4steps-lora-rank64-Seko-V1_low_noise_model
url = "https://drive.google.com/uc?id=1_08gg9FJLOlOrzovNVTEyTXsvylI7YXo"
output = "/workspace/DiffuserFlux/lora_wan_lightining-low.safetensors"
gdown.download(url, output, quiet=False)
