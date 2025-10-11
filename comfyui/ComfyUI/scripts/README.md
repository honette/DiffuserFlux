# 🧩 Wan2.2 バッチ生成システム（RunPod用）

このプロジェクトは、RunPod 上の **ComfyUI + Wan2.2** ワークフローを

ローカル PC から一括制御し、画像→動画を自動生成する仕組みです。

---

## 📁 ファイル構成

```
.
├── remote_batch_control.py   # ローカルからRunPodを制御するスクリプト
├── batch_i2v.py              # RunPod内で実際にComfyUI APIを叩くスクリプト
├── video_wan2_2_14B_i2v.json # ComfyUIワークフローテンプレート
├── input_images/             # 処理対象画像を置く
├── output/                   # rsyncで取得される生成動画
└── logs/                     # 実行ログ（ローカル・リモート双方）
```

---

## 🚀 実行の流れ

### ① RunPod 側（サーバー内）

1. Pod を起動
    - テンプレート: **Wan2.2**
    - ポート:
        - 8080 → File Manager
        - 8188 → ComfyUI API
        - SSH ポート（例: 22020）
2. 下記の2ファイルを配置
    
    ```
    /workspace/runpod-slim/ComfyUI/scripts/batch_i2v.py
    /workspace/runpod-slim/ComfyUI/video_wan2_2_14B_i2v.json
    ```
    
3. 画像をアップロード
    
    ```
    /workspace/runpod-slim/ComfyUI/input_images/
    ```
    

---

### ② ローカル 側（制御PC）

1. **必要パッケージをインストール**
    
    ```bash
    pip install paramiko pillow requests
    ```
    
2. **SSH接続可能にしておく**
    - RunPod側のPodを`SSH Enabled`で起動
    - 公開鍵をRunPod側の`~/.ssh/authorized_keys`に登録
3. **スクリプトを実行**
    
    ```bash
    python3 remote_batch_control.py <IP>:<SSH_PORT> --total <画像総数>
    ```
    
    例：
    
    ```bash
    python3 remote_batch_control.py 63.141.33.29:22020 --total 100
    ```
    
    ✅ 実行内容：
    
    - `batch_i2v.py` をSSH経由で呼び出し
    - 20枚ずつ自動で処理（limit=20固定）
    - 各バッチ終了後に rsync で動画をローカルへ同期
    - resume も常に有効（中断しても続きから再開）

4. **生成動画が同期されるディレクトリ**
    
    ```
    output/<IP>/i2v_*.mp4
    ```
    
5. **ログ**

- RunPod 内: `/workspace/runpod-slim/ComfyUI/logs/`
- ローカル: `logs/run_<IP>_<timestamp>.log`

## 🧠 特徴

| 機能 | 説明 |
| --- | --- |
| 🧩 自動バッチ制御 | 画像総数に応じて `--skip` / `--limit` を自動計算 |
| 🔁 resume機能 | 前回ログを参照して未処理ファイルだけ再実行 |
| 🔄 自動rsync | 各バッチ終了後に生成動画をローカルへ転送 |
| 📏 縦横自動判定 | 画像の縦横比に応じて解像度（960×640 / 640×960）を動的変更 |
| 🧾 詳細ログ | 各処理のステータス、解像度判定結果、rsync内容をログ出力 |

---

## 🧩 各スクリプトの役割

### `batch_i2v.py`（RunPod側）

- ComfyUI の API（ポート8188）に直接リクエストを送る。
- 画像を順に処理し、
    - 縦長／横長／正方形を自動判定
    - `WanImageToVideo` ノードの出力サイズを変更
    - 結果を `/workspace/runpod-slim/ComfyUI/video/ComfyUI/` に保存。

実行例（Pod内で）：

```bash
python3 /workspace/runpod-slim/ComfyUI/scripts/batch_i2v.py --limit 20 --skip 0

```

---

### `remote_batch_control.py`（ローカル側）

- SSH 経由で `batch_i2v.py` を複数回実行。
- 20枚ずつ順番に処理、バッチ終了ごとに結果をダウンロード。

実行例（ローカルPC）：

```bash
python3 remote_batch_control.py 63.141.33.29:22020 --total 100
```

---

## 💡 推奨ワークフロー

1. Pod 起動
2. 画像アップロード
3. ローカルから制御スクリプト実行
4. 処理完了後に Pod 停止（課金停止）

---

## 🧾 ログ例

```
🕓 Start 2025-10-11 | Target=63.141.33.29:22020
📦 Total 100 files → 5 batches
🚀 [Batch 1/5] Executing: batch_i2v.py --limit 20 --skip 0 --resume
[1] cat001.jpg: portrait/square 1080x1920 → 640x960
✅ Batch 1/5 completed OK
⬇️ Rsync output: rsync -az ...
...
🏁 All batches finished.
```

---

## 🧹 終了時の注意

- 結果をローカルへ取り込み済みなら、Podを必ず「Stop」して課金停止。
- RunPod 側の `/workspace/runpod-slim/ComfyUI/video/ComfyUI/` は容量を圧迫するので、定期的に削除推奨。
