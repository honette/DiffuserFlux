import os
import gdown
import zipfile

# 保存先ディレクトリ（存在しなければ作る）
base_dir = "/workspace/DiffuserFlux/batch"
os.makedirs(base_dir, exist_ok=True)

# Google Drive ファイルのURL
url = "https://drive.google.com/uc?id=1Cvh7mIwnvUIZxdrGsxW8Q71JhJYtYhNM"

# ダウンロード先ZIPファイル
zip_path = os.path.join(base_dir, "images.zip")

print(f"⬇️  Downloading ZIP from Google Drive ...")
gdown.download(url, zip_path, quiet=False)

# 展開先
extract_dir = os.path.join(base_dir, "source_images")
os.makedirs(extract_dir, exist_ok=True)

print(f"📦  Extracting to {extract_dir} ...")
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(extract_dir)

print("✅ Done! Extracted images:")
for f in os.listdir(extract_dir):
    print(" -", f)
