import gdown

# clothes_remover_v0
url = "https://drive.google.com/uc?id=1mL4FiKlkTqEJ6-K1f05ISTqPh3wui0j1"
# JD3s_Nudify_Kontext
#url = "https://drive.google.com/uc?id=1LJ9Xa2BrvT8i2h_sr_oBEbDDZdEWn4U6"
# NSFW V3
#url = "https://drive.google.com/uc?id=1evQqmVHCpDNRM4ehiA-SVlpFUUkOSvpr"
# FLUXTASTIC_V3
#url = "https://drive.google.com/uc?id=1oblgf_aC6qDjg-5A3MswVfqWqEKxuoFO"

output = "/workspace/DiffuserFlux/lora_model.safetensors"
gdown.download(url, output, quiet=False)
