
import asyncio
import json
import os
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import edge_tts

W, H = 1080, 1920
OUT = Path("output")
OUT.mkdir(exist_ok=True)

EPISODE = {
    "case": "CASE 001",
    "part": 1,
    "title": "THE LOCKED ROOM",
    "narration": (
        "At exactly two thirteen A M, the famous Blue Moon Diamond vanished. "
        "The mansion was locked from the inside. Every window was sealed. "
        "Three suspects were still inside the house. "
        "Detective Paws noticed something strange near the fireplace. "
        "A tiny drop of water... in a room where nothing was wet. "
        "Whoever took the diamond had made one mistake. "
        "But what was it? Find out in Part Two."
    ),
    "scenes": [
        ("2:13 A.M.", "A diamond vanished from a locked mansion."),
        ("NO WAY IN. NO WAY OUT.", "Every door was locked. Every window was sealed."),
        ("THREE SUSPECTS.", "The owner. The guest. The housekeeper."),
        ("ONE STRANGE CLUE.", "A tiny drop of water beside the fireplace."),
        ("WHO MADE THE MISTAKE?", "The investigation continues in Part 2...")
    ]
}


def font(size, bold=False):
    path = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def centered(draw, text, y, fnt, fill,
             max_width=940, spacing=12):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word

    if line:
        lines.append(line)

    for item in lines:
        box = draw.textbbox((0, 0), item, font=fnt)
        x = (W - (box[2] - box[0])) // 2
        draw.text(
            (x, y), item, font=fnt, fill=fill,
            stroke_width=2, stroke_fill="#101827"
        )
        y += (box[3] - box[1]) + spacing


def panda(draw, cx, cy, scale=1):
    r = int(190 * scale)

    # Panda face
    draw.ellipse(
        (cx-r, cy-r, cx+r, cy+r),
        fill="#f7f7f2", outline="#111827", width=12
    )

    # Ears
    er = int(65 * scale)
    draw.ellipse(
        (cx-r//2-er, cy-r-er//2,
         cx-r//2+er, cy-r+er//2),
        fill="#101827"
    )
    draw.ellipse(
        (cx+r//2-er, cy-r-er//2,
         cx+r//2+er, cy-r+er//2),
        fill="#101827"
    )

    # Eye patches
    draw.ellipse(
        (cx-int(125*scale), cy-int(55*scale),
         cx-int(25*scale), cy+int(70*scale)),
        fill="#101827"
    )
    draw.ellipse(
        (cx+int(25*scale), cy-int(55*scale),
         cx+int(125*scale), cy+int(70*scale)),
        fill="#101827"
    )

    # Eyes and nose
    draw.ellipse(
        (cx-int(85*scale), cy-int(5*scale),
         cx-int(55*scale), cy+int(25*scale)),
        fill="white"
    )
    draw.ellipse(
        (cx+int(55*scale), cy-int(5*scale),
         cx+int(85*scale), cy+int(25*scale)),
        fill="white"
    )
    draw.ellipse(
        (cx-int(22*scale), cy+int(65*scale),
         cx+int(22*scale), cy+int(95*scale)),
        fill="#101827"
    )

    # Detective hat
    draw.rounded_rectangle(
        (cx-int(155*scale), cy-r-int(70*scale),
         cx+int(155*scale), cy-r-int(5*scale)),
        radius=18, fill="#6b4f35",
        outline="#111827", width=8
    )
    draw.rectangle(
        (cx-int(180*scale), cy-r-int(15*scale),
         cx+int(180*scale), cy-r+int(10*scale)),
        fill="#4b3627"
    )


def make_scene(index, headline, subline):
    im = Image.new("RGB", (W, H), "#101827")
    d = ImageDraw.Draw(im)

    # Night background
    for y in range(H):
        t = y / H
        col = (
            int(9 + 12*t),
            int(17 + 13*t),
            int(32 + 22*t)
        )
        d.line((0, y, W, y), fill=col)

    # Moon and mansion
    d.ellipse((760, 170, 980, 390), fill="#d9e2e8")
    d.rectangle((0, 1120, W, 1920), fill="#090f1b")

    d.polygon(
        [(80,1120), (80,850), (260,730),
         (440,850), (440,1120)],
        fill="#182536"
    )
    d.polygon(
        [(590,1120), (590,820), (820,700),
         (1030,820), (1030,1120)],
        fill="#182536"
    )

    for x in [150, 250, 680, 800, 920]:
        d.rectangle((x, 900, x+55, 1000), fill="#d49a48")

    # Panda detective
    d.ellipse(
        (190,700,890,1400),
        outline="#263b50", width=8
    )
    panda(d, 540, 970, 1.05)

    # Text
    centered(
        d, "PANDA DETECTIVE", 120,
        font(48, True), "#f2c879"
    )
    centered(
        d, headline, 1450,
        font(66, True), "#ffffff", 960, 16
    )
    centered(
        d, subline, 1635,
        font(39), "#d7e2ef", 930, 14
    )
    centered(
        d, "CASE 001  •  PART 01  •  SCENE "
        + str(index+1) + "/5",
        1830, font(25, True), "#f2c879"
    )

    path = OUT / f"scene_{index:02d}.png"
    im.save(path)
    return path


async def make_voice(text, path):
    voice = os.getenv("TTS_VOICE", "en-US-GuyNeural")
    communicate = edge_tts.Communicate(
        text, voice, rate="-5%", volume="+0%"
    )
    await communicate.save(str(path))


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    OUT.mkdir(exist_ok=True)

    scene_files = [
        make_scene(i, headline, subline)
        for i, (headline, subline)
        in enumerate(EPISODE["scenes"])
    ]

    audio = OUT / "voice.mp3"
    asyncio.run(make_voice(EPISODE["narration"], audio))

    clips = []

    for i, img in enumerate(scene_files):
        clip = OUT / f"clip_{i:02d}.mp4"

        run([
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(img),
            "-t", "7",
            "-vf",
            "scale=1080:1920,zoompan="
            "z='min(zoom+0.0005,1.04)':"
            "d=175:s=1080x1920:fps=25,format=yuv420p",
            "-r", "25",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            str(clip)
        ])

        clips.append(clip)

    concat = OUT / "concat.txt"
    concat.write_text(
        "".join(
            f"file '{p.resolve()}'\n"
            for p in clips
        )
    )

    silent = OUT / "silent.mp4"

    run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat),
        "-c", "copy",
        str(silent)
    ])

    final = OUT / "Panda_Detective_Case001_Part01.mp4"

    run([
        "ffmpeg", "-y",
        "-i", str(silent),
        "-i", str(audio),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-af", "apad",
        "-shortest",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        str(final)
    ])

    metadata = {
        "title": "The Locked Room | Panda Detective | Case 001 Part 1 #Shorts",
        "description": (
            "A diamond vanished from a locked mansion. "
            "Detective Paws finds one impossible clue. "
            "Part 2 coming soon. "
            "#mystery #detective #animation #shorts"
        ),
        "tags": [
            "Panda Detective",
            "mystery",
            "detective story",
            "animated shorts",
            "shorts"
        ]
    }

    (OUT / "metadata.json").write_text(
        json.dumps(metadata, indent=2)
    )

    print(f"Created: {final}")


if __name__ == "__main__":
    main()
