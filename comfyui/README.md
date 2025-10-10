## セットアップ

- モデルのダウンロード（ターミナルから）

```bash
cd /workspace
git clone https://github.com/honette/DiffuserFlux.git
cd DiffuserFlux/comfyui
pip install tqdm
python3 pull_wan_diffuser_model_for_comfyui.py
```

## プロンプト

### Systemプロンプト

- Constraints: head orientation remains constant throughout the motion; Camera: fixed front, The composition does not change; Mood: She is teenager, She has large nipples;
- Constraints: head orientation remains constant throughout the motion; Camera: Zoom out so that the camera covers her from head to waist; Mood: She keeps expression. She is teenager,She has large nipples, her breasts are so soft;

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
- 第三者がすれ違いざまに脱がす（すれ違いざまに)
    - Description: She stands still as an unseen figure swiftly crosses the frame from right to left, stripping her clothes to become completely naked;
    - Description: She stands still as an unseen figure swiftly passes from the right side of the frame, tearing away her clothes in a single fluid motion, becomes completely naked; the figure exits the frame to the left;
- 服がバラバラになる（縫い目から分断）
    - Description: Her clothes seams unravel, splitting into shaped fabrics that fall apart, revealing her naked body; the fabric pieces drop slowly, retaining their cutout forms;  
- 服が溶ける（分解）
    - Description: Her clothes dissolve into sparkling particles, gradually revealing her naked body;
    - Description: Her clothes dissolve into shimmering particles, gradually revealing her naked body; the dissolution starts from the edges and moves inward, like fabric melting into light;
- 服が溶ける（酸）
    - Description: Her clothes erode with acid-like holes, becomes completely naked;
    - Description: Her clothes erode as if by acid, forming holes that spread randomly, becomes completely naked; the fabric dissolves completely, leaving no traces;
- 服が溶ける（絵具）
    - Description: Her jacket melts into vibrant liquid paint, dripping down her body, revealing her naked body; the colors stream slowly, fading into the floor;
- 服が風によって裂かれる
    - Description: A sudden gust rips her clothes into fragments, scattering them, becomes completely naked;
    - Description: Sudden gust of wind tears her clothes into fragments, scattering them like pieces, becomes completely naked; the fabric pieces flutter briefly before disappearing;
- 服が風で吹き飛ぶ
    - Description: A sudden gust carries her clothes away, becomes completely naked;
    - Description: A sudden gust of wind sweeps her clothes away, carrying the clothes whole out of the frame, becomes completely naked;
- 服が蝶となり飛んでいく
    - Description: Her clothes transforms into countless butterflies in a magical flourish, fluttering away in a vibrant swarm, becomes completely naked; the butterflies scatter and vanish;
- トランジションで徐々に脱げる
    - Description: Her outfit changes from underwear to lingerie to complete nudity with each strobing flash, and she poses like a fashion model with each outfit change.
- ビームで服に穴が開く
    - Description: A searing beam strikes her jacket, burning a large hole at the chest, revealing her unharmed naked body, breasts and nipples;
- 服が水にぬれて（ビニールのように）透明になる
    - Description: As her clothes get wet, they become transparent like vinyl, gradually revealing her naked body, breasts, and nipples;

### Partical Scene ideas

- Scene 1/2: Her jacket blasts off in a burst of wind, vanishing instantly, revealing her naked body;
- Scene 2/2: She spins gracefully, turning fully, ending with a poised stance;  
