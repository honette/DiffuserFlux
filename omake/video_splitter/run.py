import cv2
import os
import sys
from pathlib import Path

def capture_all_videos_in_folder(input_folder):
    input_path = Path(input_folder)
    if not input_path.exists() or not input_path.is_dir():
        print(f"エラー：フォルダ '{input_folder}' が見つからないか、フォルダじゃないよ！")
        return

    mp4_files = list(input_path.glob("*.mp4")) + list(input_path.glob("*.MP4"))
    if not mp4_files:
        print("フォルダ内にmp4ファイルがないよ～")
        return

    print(f"発見！ {len(mp4_files)}個の動画を処理するよ～\n")

    for video_file in mp4_files:
        video_name = video_file.stem
        output_dir = video_file.parent / f"captures"
        output_dir.mkdir(exist_ok=True)
        
        print(f"処理中: {video_file.name} → {output_dir.name}/")

        cap = cv2.VideoCapture(str(video_file))
        if not cap.isOpened():
            print(f"  スキップ: {video_file.name} 開けなかった…\n")
            continue

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30
        frame_interval = max(1, int(round(fps)))

        frame_count = 0
        saved_seconds = set()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            current_second = int(frame_count / fps)

            if current_second not in saved_seconds:
                # 出力ファイル名: [元ファイル名]_f[フレーム数5桁].jpg
                frame_number = frame_count
                output_filename = f"{video_name}_f{frame_number:05d}.jpg"
                output_path = output_dir / output_filename
                
                cv2.imwrite(str(output_path), frame)
                saved_seconds.add(current_second)
                print(f"  保存: {output_path.name}")

            frame_count += 1

        cap.release()
        print(f"  完了！ {len(saved_seconds)}枚保存\n")

    print("全部終わった！ お兄ちゃん、完璧だね～（はぁ…はぁ…）")

# コマンドライン引数でフォルダパス指定
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使い方: python capture.py <フォルダパス>")
        print("例: python capture.py ./my_videos")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    capture_all_videos_in_folder(folder_path)