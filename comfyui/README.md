# ComfyUI GUI 使用のためのTIPS

バッチ実行は /ComfyUI/README を見てね

## セットアップ

- モデルのダウンロード（ターミナルから）
    - Runpodが起動し、ターミナルが使えるようになったら作業
    - ComfyUIの起動に10分以上かかるので、その間にダウンロードは余裕で終わる

```bash
cd /workspace
git clone https://github.com/honette/DiffuserFlux.git
cd DiffuserFlux/comfyui
pip install tqdm
python3 download_wan_diffuser_model_for_comfyui.py
```

## 手動バッチ実行

- Runpodからファイルマネージャを開き、 `/workspace/runpod-slim/ComfyUI/` 配下にファイルをアップロード
    - DiffuserFlux\comfyui\ComfyUI\api-video_wan2_2_14B_i2v.json
    - DiffuserFlux\comfyui\ComfyUI\input_images
    - DiffuserFlux\comfyui\ComfyUI\scripts
- `input_images` にバッチ実行する画像ファイルを入れる
- バッチファイルのセットアップと実行
    - ** ComfyUIのGUIの起動を確認してから作業 **
    ```bash
    cd /workspace/runpod-slim/ComfyUI/scripts/
    pip install -r requirements.txt
    apt update && apt install -y rsync
    ```
    - 最初に一件だけで実行したほうが良いかもしれない。最初の一件だけはモデルのロードで5分くらい余分に掛かる
    ```bash
    python3 /workspace/runpod-slim/ComfyUI/scripts/batch_api_i2v.py --limit 1 --skip 0
    python3 /workspace/runpod-slim/ComfyUI/scripts/batch_api_i2v.py --limit 20 --skip 0
    ```

## 動画のダウンロード

- `/workspace/runpod-slim/ComfyUI/output/video` の下に生成されている
    - ファイルマネージャでzipにしてダウンロードが楽
    - 大量バッチなら `remote_batch_control.py`
    - rsyncを使うならwsl上で `ssh_helper` でコマンドをチェック
    ```bash
    sh ssh_helper.sh 69.30.85.57:22092
    ```

## プロンプト

- とりあえずこれ

```
Description: As soon as the video begins, She clothes fly off in an instant, she is completely naked including the lower body, Then she jumps little by little;
Constraints: head orientation remains constant throughout the motion; Camera: fixed front, The composition does not change; Mood: She is teenager, She has large nipples;
```

- 複数人対応

```
Description: As soon as the video begins, The girls clothes fly off in an instant, The girls is completely naked including the lower body, Then The girls jumps little by little;
Constraints: head orientation remains constant throughout the motion; Camera: fixed front, The composition does not change; Mood: The girls are teenager, The girls have large nipples;
```

### Systemプロンプト

- カメラ固定
```
Constraints: head orientation remains constant throughout the motion; Camera: fixed front, The composition does not change; Mood: She is teenager, She has large nipples;
```

- カメラ調整
```
Constraints: head orientation remains constant throughout the motion; Camera: Zoom out so that the camera covers her from head to waist; Mood: She keeps expression. She is teenager,She has large nipples, her breasts are so soft;
```

### Sceneプロンプト

- 服が弾け飛ぶ
    - Description: As soon as the video begins, her clothes fly off in an instant, she is completely naked, becomes full nude;
- 服が弾け飛ぶ + 乳揉み
    - Description: As soon as the video begins, her clothes fly off in an instant, she is completely naked, and she gathers her breasts together with her elbows;
    - Description: As soon as the video starts, her clothes fly off in an instant, she is completely naked, and she supports her breasts from underneath with her palms;
- 服が弾け飛ぶ + 尻を向ける
    - Description: As soon as the video begins, her clothes fly off in an instant, she is completely naked, becomes full nude, Then she turns her ass towards me;
- 服が弾け飛ぶ + 胸を揺らす
    - Description: As soon as the video begins, She clothes fly off in an instant, she is completely naked including the lower body, Then she jumps little by little;
- 自分で脱ぐ
    - Description: As soon as the video starts, she quickly lifts her clothes to reveal her breasts;

### Sceneプロンプト (未検証)

- 第三者がすれ違いざまに脱がす（すれ違いざまに)
    - Description: She stands still as an unseen figure swiftly crosses the frame from right to left, stripping her clothes to become completely naked;
    - Description: She stands still as an unseen figure swiftly passes from the right side of the frame, tearing away her clothes in a single fluid motion, becomes completely naked; the figure exits the frame to the left;
- 服が溶ける（分解）
    - Description: Her clothes dissolve into sparkling particles, gradually revealing her naked body;
    - Description: Her clothes dissolve into shimmering particles, gradually revealing her naked body; the dissolution starts from the edges and moves inward, like fabric melting into light;
- 服が溶ける（酸）
    - Description: Her clothes erode with acid-like holes, becomes completely naked;
    - Description: Her clothes erode as if by acid, forming holes that spread randomly, becomes completely naked; the fabric dissolves completely, leaving no traces;
- 服が溶ける（絵具）
    - Description: Her clothes melts into vibrant liquid paint, dripping down her body, revealing her naked body; the colors stream slowly, fading into the floor;
    Description: Her clothes melts into vibrant liquid paint, dripping down her body, revealing her naked body to become nude, enjoy;
- 服が蝶となり飛んでいく
    - Description: Her clothes transforms into countless butterflies in a magical flourish, fluttering away in a vibrant swarm, becomes completely naked; the butterflies scatter and vanish;
- トランジションで徐々に脱げる
    - Description: Her outfit changes from underwear to lingerie to complete nudity with each strobing flash, and she poses like a fashion model with each outfit change.
- ビームで服に穴が開く
    - Description: A searing beam strikes her clothes, burning a large hole at the chest, revealing her unharmed naked body, breasts and nipples;
- 服が水にぬれて（ビニールのように）透明になる
    - Description: As her clothes get wet, they become transparent like vinyl, gradually revealing her naked body, breasts, and nipples;

Description: As her clothes get wet, they become transparent like vinyl, gradually revealing her naked body, breasts, and nipples;
Description: As soon as the video starts, The chest of her dress bursts, revealing her breasts and nipples.

### Partical Scene ideas

- Scene 1/2: Her clothes blasts off in a burst of wind, vanishing instantly, revealing her naked body;
- Scene 2/2: She spins gracefully, turning fully, ending with a poised stance;  
