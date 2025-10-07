# 🚀 RunPod 上で Flux1.Kontact + Diffusers 環境構築手順

- SSH接続、SCPダウンロード (アドレスは適宜変更）

```bash
ssh root@194.68.245.146 -p 22119 -i ~/.ssh/id_runpod
# scp -i ~/.ssh/id_runpod -P 22119 -r root@194.68.245.146:/workspace/DiffuserFlux/tmp/*.png ./
rsync -avz -e "ssh -i ~/.ssh/id_runpod -p 22119" root@194.68.245.146:/workspace/DiffuserFlux/tmp/ ./

```

## 1. 作業環境構築

```bash
apt update; apt install -y vim
cd /workspace
git clone https://github.com/honette/DiffuserFlux.git
cd DiffuserFlux/

# venv環境にライブラリをインストール
bash setup.sh

# venvを使わない場合
pip install -r requirements.txt
```

## トラブルシューティング

```
# ターミナルがフリーズ、プロセスだけが残った
ps aux | grep python
kill 1234

```

---

## Sample Prompt

何を維持して、何を変更するのかを明確にするのがポイント

- モデルも構図もそのまま、服装とポーズの変更
  - The woman playing at beach. Change her outfit to a bikini swimsuit. she posing excited her both arms up.

- モデルだけそのまま、元の構図を無視させる
  - This female model is in a completely different cinematic scene. Change to a stylish pose like in a fashion magazine. Change her outfit to a bikini swimsuit.
