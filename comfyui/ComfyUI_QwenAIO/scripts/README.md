- **SaveImageノードの準備**
送ってくれたJSONだと、出力が **`PreviewImage` (ID: 6)** になっていたよ。
APIでファイル保存を確実にするには、ComfyUI上で `PreviewImage` を削除して **`SaveImage`** ノードを追加し、そのIDをスクリプト内の `save_id` に設定してね。
- **`image1` と `image2` のリンク**
Qwenの `TextEncodeQwenImageEditPlus` (ID: 3) ノードには、`image1` (リンク17) と `image2` (リンク18) が繋がっているのを確認したよ。
    - **`image1`**: ループで回す画像がここに入るようにしているよ。
    - **`image2`**: 固定で使いたい背景や参照画像がある場合は、`config_qwen.json` にパスを書いてね。
- **ヒアリング：解像度の固定について**
元のスクリプトでは `640x640` などにリサイズしていたけど、Qwenは入力画像のサイズに合わせるのが一般的かな？今回は入力画像のサイズをそのまま `EmptyLatentImage` に渡すようにしたけど、特定のサイズ（例えば1024固定など）にしたい場合は教えてね！
