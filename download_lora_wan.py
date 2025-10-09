import gdown

# NSFW-22-H-e8 (NSFW V2.2 Hentai)
url = "https://drive.google.com/uc?id=1-CKoRMcb5tB-K7AfrZg5AGriwAz9fnwC"

output = "/workspace/DiffuserFlux/lora_flux_nsfw.safetensors"
gdown.download(url, output, quiet=False)
