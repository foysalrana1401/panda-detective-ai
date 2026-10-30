import os
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# =====================================
# SETTINGS
# =====================================

WIDTH = 720
HEIGHT = 1280
FPS = 30
SCENE_SECONDS = 7

BASE = Path(__file__).resolve().parent
OUT = BASE / "output"
FRAMES = OUT / "frames"
CLIPS = OUT / "clips"

OUT.mkdir(exist_ok=True)
FRAMES.mkdir(exist_ok=True)
CLIPS.mkdir(exist_ok=True)


# =====================================
# EPISODE STORY
# =====================================

EPISODE = {
    "title": "THE MYSTERY OF THE EMPTY MANSION",
    "case": "CASE 001",
    "narration": (
        "At midnight, Detective Panda received a strange message. "
        "A mansion had been locked for twenty years. "
        "But tonight, someone had turned on the lights. "
        "Panda entered the dark mansion and found muddy footprints. "
        "Suddenly, a shadow moved behind him. "
        "Who was inside the mansion? "
        "The mystery had only just begun."
    ),
    "scenes": [
        {
            "title": "A STRANGE MESSAGE",
            "subtitle": "12:00 AM. A mysterious message arrives.",
            "bg": (15, 24, 54),
        },
        {
            "title": "THE EMPTY MANSION",
            "subtitle": "Nobody has lived here for twenty years.",
            "bg": (25, 30, 65),
        },
        {
            "title": "MUDDY FOOTPRINTS",
            "subtitle": "Someone entered the mansion tonight.",
            "bg": (34, 25, 48),
        },
        {
            "title": "A SHADOW MOVES",
            "subtitle": "Panda hears something behind him...",
            "bg": (10, 12, 30),
        },
        {
            "title": "WHO IS INSIDE?",
            "subtitle": "To be continued...",
            "bg": (18, 20, 48),
        },
    ],
}


# =====================================
# FONT
# =====================================

def get_font(size):
    possible_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]

    for font_path in possible_fonts:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)

    return ImageFont.load_default()


# =====================================
# DRAW PANDA CHARACTER
# =====================================

def draw_panda(draw, cx, cy, scale=1.0):

    # Body
    draw.ellipse(
        (
            cx - 95 * scale,
            cy + 70 * scale,
            cx + 95 * scale,
            cy + 270 * scale,
        ),
        fill=(245, 245, 245),
        outline=(20, 20, 25),
        width=5,
    )

    # Ears
    draw.ellipse(
        (
            cx - 100 * scale,
            cy - 100 * scale,
            cx - 20 * scale,
            cy - 20 * scale,
        ),
        fill=(15, 15, 20),
    )

    draw.ellipse(
        (
            cx + 20 * scale,
            cy - 100 * scale,
            cx + 100 * scale,
            cy - 20 * scale,
        ),
        fill=(15, 15, 20),
    )

    # Head
    draw.ellipse(
        (
            cx - 100 * scale,
            cy - 90 * scale,
            cx + 100 * scale,
            cy + 110 * scale,
        ),
        fill=(250, 250, 250),
        outline=(20, 20, 25),
        width=5,
    )

    # Eyes
    draw.ellipse(
        (
            cx - 72 * scale,
            cy - 35 * scale,
            cx - 15 * scale,
            cy + 35 * scale,
        ),
        fill=(15, 15, 20),
    )

    draw.ellipse(
        (
            cx + 15 * scale,
            cy - 35 * scale,
            cx + 72 * scale,
            cy + 35 * scale,
        ),
        fill=(15, 15, 20),
    )

    # Eye highlights
    draw.ellipse(
        (
            cx - 48 * scale,
            cy - 20 * scale,
            cx - 32 * scale,
            cy - 4 * scale,
        ),
        fill="white",
    )

    draw.ellipse(
        (
            cx + 38 * scale,
            cy - 20 * scale,
            cx + 54 * scale,
            cy - 4 * scale,
        ),
        fill="white",
    )

    # Nose
    draw.ellipse(
        (
            cx - 15 * scale,
            cy + 30 * scale,
            cx + 15 * scale,
            cy + 52 * scale,
        ),
        fill=(10, 10, 10),
    )

    # Detective hat
    draw.rectangle(
        (
            cx - 110 * scale,
            cy - 110 * scale,
            cx + 110 * scale,
            cy - 85 * scale,
        ),
        fill=(100, 65, 35),
    )

    draw.polygon(
        [
            (cx - 75 * scale, cy - 110 * scale),
            (cx - 50 * scale, cy - 165 * scale),
            (cx + 50 * scale, cy - 165 * scale),
            (cx + 75 * scale, cy - 110 * scale),
        ],
        fill=(120, 80, 40),
    )


# =====================================
# DRAW MANSION
# =====================================

def draw_mansion(draw):

    # Main building
    draw.rectangle(
        (130, 420, 590, 900),
        fill=(45, 43, 58),
        outline=(10, 10, 20),
        width=8,
    )

    # Roof
    draw.polygon(
        [
            (90, 430),
            (360, 220),
            (630, 430),
        ],
        fill=(25, 25, 40),
        outline=(5, 5, 10),
    )

    # Windows
    for x in [205, 430]:
        draw.rectangle(
            (x, 510, x + 90, 650),
            fill=(255, 190, 70),
            outline=(10, 10, 10),
            width=6,
        )

        draw.line(
            (x + 45, 510, x + 45, 650),
            fill=(30, 25, 20),
            width=5,
        )

        draw.line(
            (x, 580, x + 90, 580),
            fill=(30, 25, 20),
            width=5,
        )

    # Door
    draw.rectangle(
        (300, 700, 420, 900),
        fill=(20, 18, 28),
        outline=(5, 5, 10),
        width=6,
    )

    draw.ellipse(
        (390, 790, 405, 805),
        fill=(240, 190, 70),
    )


# =====================================
# CREATE SCENE IMAGE
# =====================================

def make_scene(index, scene):

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        scene["bg"],
    )

    draw = ImageDraw.Draw(image)

    # Background stars
    for x in range(35, WIDTH, 110):
        for y in range(80, 400, 120):
            draw.ellipse(
                (x, y, x + 5, y + 5),
                fill=(180, 190, 220),
            )

    # Moon
    draw.ellipse(
        (510, 100, 640, 230),
        fill=(245, 225, 170),
    )

    # Mansion
    draw_mansion(draw)

    # Panda
    if index in [0, 1, 3, 4]:
        draw_panda(draw, 360, 920, 0.85)

    # Footprints
    if index == 2:
        for i in range(5):
            x = 230 + i * 55
            y = 850 - i * 65

            draw.ellipse(
                (x, y, x + 25, y + 45),
                fill=(15, 15, 20),
            )

    # Shadow
    if index == 3:
        draw.ellipse(
            (470, 750, 650, 1080),
            fill=(5, 5, 12),
        )

    # Top label
    draw.rounded_rectangle(
        (35, 35, 685, 115),
        radius=20,
        fill=(10, 10, 25),
    )

    draw.text(
        (60, 55),
        EPISODE["case"],
        font=get_font(32),
        fill=(255, 205, 80),
    )

    # Scene title
    title_font = get_font(38)

    draw.rounded_rectangle(
        (25, 1080, 695, 1235),
        radius=25,
        fill=(8, 10, 25),
    )

    draw.text(
        (50, 1095),
        scene["title"],
        font=title_font,
        fill=(255, 215, 110),
    )

    # Subtitle
    draw.text(
        (50, 1160),
        scene["subtitle"],
        font=get_font(21),
        fill=(240, 240, 240),
    )

    image.save(FRAMES / f"scene_{index:02d}.png")


# =====================================
# CREATE VOICE
# =====================================

def make_voice(text, path):

    subprocess.run(
        [
            "espeak-ng",
            "-v", "en-us",
            "-s", "145",
            "-w", str(path),
            text,
        ],
        check=True,
    )


# =====================================
# CREATE VIDEO CLIPS
# =====================================

def make_video_clip(index):

    image_path = FRAMES / f"scene_{index:02d}.png"
    clip_path = CLIPS / f"clip_{index:02d}.mp4"

    total_frames = FPS * SCENE_SECONDS

    zoom_filter = (
        f"zoompan=z='min(zoom+0.0005,1.08)':"
        f"d={total_frames}:"
        f"s={WIDTH}x{HEIGHT}:"
        f"fps={FPS},"
        f"format=yuv420p"
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-vf", zoom_filter,
            "-t", str(SCENE_SECONDS),
            "-r", str(FPS),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(clip_path),
        ],
        check=True,
    )

    return clip_path


# =====================================
# JOIN VIDEO CLIPS
# =====================================

def join_clips():

    list_file = OUT / "clips.txt"

    with open(list_file, "w", encoding="utf-8") as file:
        for index in range(len(EPISODE["scenes"])):
            clip = CLIPS / f"clip_{index:02d}.mp4"
            file.write(f"file '{clip.resolve()}'\n")

    silent_video = OUT / "silent_video.mp4"

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(list_file),
            "-c", "copy",
            str(silent_video),
        ],
        check=True,
    )

    return silent_video


# =====================================
# ADD VOICE TO VIDEO
# =====================================

def add_audio(video, audio):

    final_video = OUT / "Panda_Detective_Case001_Part01.mp4"

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", str(video),
            "-i", str(audio),
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-af", "apad",
            "-shortest",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            str(final_video),
        ],
        check=True,
    )

    return final_video


# =====================================
# MAIN PROGRAM
# =====================================

def main():

    print("PANDA DETECTIVE VIDEO BUILDER STARTED")

    # Create scene images
    for index, scene in enumerate(EPISODE["scenes"]):
        print(f"Creating scene {index + 1}...")
        make_scene(index, scene)

    # Create voice
    print("Creating detective voice...")

    audio = OUT / "voice.wav"
    make_voice(EPISODE["narration"], audio)

    # Create video clips
    for index in range(len(EPISODE["scenes"])):
        print(f"Rendering video clip {index + 1}...")
        make_video_clip(index)

    # Join clips
    print("Joining video scenes...")

    silent_video = join_clips()

    # Add voice
    print("Adding voice to video...")

    final_video = add_audio(silent_video, audio)

    print("VIDEO CREATED SUCCESSFULLY!")
    print(f"Output file: {final_video}")


if __name__ == "__main__":
    main()
