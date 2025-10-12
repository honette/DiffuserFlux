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
- ComfyUIのGUIをRunpodから開く
    - Runpodのログにセットアップ完了的なメッセージが出てる
    - ワークフローはテンプレートから `Wan2.2 14B FP8 Image to Video` のやつを選択
    - 自分のやつでもOK `comfyui\ComfyUI\video_wan2_2_14B_i2v.json`
- バッチファイルのセットアップと実行
    - ** ComfyUIのGUIの起動を確認してから作業 **
    ```bash
    cd /workspace/runpod-slim/ComfyUI/scripts/
    pip install -r requirements.txt
    apt update && apt install -y rsync
    ```
    - 最初に一件だけで実行したほうが良いかもしれない。最初の一件だけはモデルのロードで5分くらい余分に掛かる
        - 注意: ワークフローがデフォルトでキュー100件までの設定
    ```bash
    python3 /workspace/runpod-slim/ComfyUI/scripts/batch_api_i2v.py --limit 1 --skip 0
    python3 /workspace/runpod-slim/ComfyUI/scripts/batch_api_i2v.py --limit 20 --skip 0
    ```

## GUI設定

- ファイル名設定は変えたほうが良い `GUI_%date:yyyy-MM-dd_HH-mm%_%model%`

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
Description: As soon as the video begins, The girls's all worn items fly off in an instant, The girls are completely naked including the lower body, also nipples and pussy, Then The girls jumps little by little;
Constraints: head orientation remains constant throughout the motion; Camera: fixed front, The composition does not change; Mood: She is teenager, She has large nipples;
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

- BASE
```
Description: As soon as the video begins, ????, then revealing her naked body, including the lower body;
```

- 服が弾け飛ぶ + 胸を揺らす
    - Description: As soon as the video begins, The girls's all worn items fly off in an instant, The girls are completely naked including the lower body, also nipples and pussy, Then The girls jumps little by little;
- 服が弾け飛ぶ + 乳揉み
    - Description: As soon as the video begins, her clothes fly off in an instant, she is completely naked, and she gathers her breasts together with her elbows;
    - Description: As soon as the video starts, her clothes fly off in an instant, she is completely naked, and she supports her breasts from underneath with her palms;
- 服が弾け飛ぶ + 尻を向ける
    - Description: As soon as the video starts, her clothes are blown off in an instant and she is completely naked, completely nude, and then she quickly turns her ass towards me;
- 自分で脱ぐ
    - Description: As soon as the video starts, she quickly lifts her clothes to reveal her breasts, nipples;
- 頭から水をかぶって服が流される
    - Description: As soon as the video begins, water pours down on her head, washing away her clothes and leaving her completely naked, including her lower body;

### Sceneプロンプト (未検証)

- 第三者が脱がす
    - Description: As soon as the video starts, A third person's arm reaches out from under the screen and rips her clothes off in an instant, she is completely naked, becomes full nude;
- 温泉に入ろう
    - As soon as the video starts, the background changes to a hot spring, and at the same time she becomes completely naked and soaks in the hot spring.

Description: As her clothes get wet, they become transparent like vinyl, gradually revealing her naked body, breasts, and nipples;
Description: As soon as the video starts, The chest of her dress bursts, revealing her breasts and nipples.
Description: In the slideshow video, she is completely naked in the center of the screen and takes various sexy poses.
### Partical Scene ideas

```
Scene 1/3: As soon as the video begins, The girls clothes fly off in an instant, The girls are completely naked including the lower body, also nipples;
Scene 2/3: She turns her ass towards me;
Scene 3/3: She faces forward, leans forward and presses her breasts together;
Constraints: head orientation remains constant throughout the motion; Camera: fixed front, The composition does not change; Mood: The girls are teenager, The girls have large nipples;

Scene 1/2: She takes off her clothes and is in her underwear;
Scene 2/2: She takes off her underwear, She is completely naked including the lower body, also nipples;
Constraints: Videos are at 2x speed; Camera: fixed front, The composition does not change; Mood: The girls are teenager, The girls have large nipples;
```