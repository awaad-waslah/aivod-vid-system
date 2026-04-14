import random
import subprocess
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
MEMES_DIR = BASE_DIR / "videos" / "memes"
TALKING_DIR = BASE_DIR / "videos" / "talking"
OUTPUT_FILE = BASE_DIR / "output.mp4"

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}

def get_videos(folder: Path) -> list[Path]:
    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")
    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTS]
    if not files:
        raise FileNotFoundError(f"No videos found in: {folder}")
    return sorted(files)

def run_ffmpeg(meme_path: Path, talking_path: Path, output_path: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(meme_path),
        "-i", str(talking_path),
        "-filter_complex", "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa]",
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_path),
    ]
    subprocess.run(cmd, check=True)

def main() -> None:
    memes = get_videos(MEMES_DIR)
    talking = get_videos(TALKING_DIR)

    meme = random.choice(memes)
    talk = random.choice(talking)

    print(f"Selected meme: {meme.name}")
    print(f"Selected talking video: {talk.name}")

    run_ffmpeg(meme, talk, OUTPUT_FILE)

    if not OUTPUT_FILE.exists():
        print("output.mp4 was not created.", file=sys.stderr)
        sys.exit(1)

    print(f"Created: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()