import gdown

# clothes_remover_v0
url = "https://drive.google.com/uc?id=1mL4FiKlkTqEJ6-K1f05ISTqPh3wui0j1"

output = "/workspace/DiffuserFlux/lora_flux_uncensored.safetensors"
gdown.download(url, output, quiet=False)

# JD3s_Nudify_Kontext
#url = "https://drive.google.com/uc?id=1LJ9Xa2BrvT8i2h_sr_oBEbDDZdEWn4U6"
# NSFW V3
#url = "https://drive.google.com/uc?id=1evQqmVHCpDNRM4ehiA-SVlpFUUkOSvpr"
# FLUXTASTIC_V3
#url = "https://drive.google.com/uc?id=1oblgf_aC6qDjg-5A3MswVfqWqEKxuoFO"
# NSFW master
url = "https://drive.google.com/uc?id=1fdJc6pH838QONfqwBsxV_xcXxcBuYOx4"

output = "/workspace/DiffuserFlux/lora_flux_nsfw.safetensors"
gdown.download(url, output, quiet=False)

# All in one nipples
url = "https://drive.google.com/uc?id=1uSquF3AroUBoDBmKx7ywBjKElHBvgcaR"
# aps nipples
url = "https://drive.google.com/uc?id=1TfkCebZYPf9TgJeMc5KpOwjWvYCrAdzp"

output = "/workspace/DiffuserFlux/lora_flux_nipples.safetensors"
gdown.download(url, output, quiet=False)

# Breasts Out Fashion
url = "https://drive.google.com/uc?id=11Q7hj6Qik9VRwJ9IPFuGmRrQ52Ta0Nyv"
output = "/workspace/DiffuserFlux/lora_flux_2bout.safetensors"
gdown.download(url, output, quiet=False)
