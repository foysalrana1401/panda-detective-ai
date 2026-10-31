
import math
import random
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


# =====================================
# PANDA DETECTIVE ANIMATION STUDIO
# Episode 1
# =====================================

W, H = 540, 960
FPS = 15
SCENE_SECONDS = 6
SCENE_COUNT = 5
TOTAL_FRAMES = FPS * SCENE_SECONDS * SCENE_COUNT

OUT = Path("studio_output")
FRAMES = OUT / "frames"
OUT.mkdir(exist_ok=True)
FRAMES.mkdir(exist_ok=True)

random.seed(12)

NARRATION = [
    "At midnight, Detective Panda received a mysterious letter.",
    "The letter came from an abandoned mansion.",
    "Inside, he discovered strange footprints and a hidden key.",
    "Suddenly, a terrifying shadow appeared behind him!",
    "Panda turned around. But the mysterious stranger had vanished. The investigation had just begun."
]

TITLES = [
    "THE MYSTERIOUS LETTER",
    "THE ABANDONED MANSION",
    "A HIDDEN CLUE",
    "THE SHADOW",
    "TO BE CONTINUED..."
]

SUBTITLES = [
    "A strange case begins at midnight.",
    "Nobody has entered for twenty years.",
    "Someone was here before Panda.",
    "Something is following our detective.",
    "Who is the mysterious stranger?"
]

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()


def draw_text_center(draw, y, text, size, color):
    f = font(size)
    box = draw.textbbox((0, 0), text, font=f)
    x = (W - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=f, fill=color)


def draw_mansion(draw, glow=0):
    # Mansion body
    draw.rectangle(
        (75, 330, 465, 710),
        fill=(37, 40, 58),
        outline=(10, 12, 25),
        width=7
    )

    # Roof
    draw.polygon(
        [(45, 345), (270, 150), (495, 345)],
        fill=(20, 23, 39)
    )

    # Towers
    draw.rectangle((95, 235, 180, 360), fill=(30, 33, 50))
    draw.polygon(
        [(85, 240), (137, 160), (190, 240)],
        fill=(18, 21, 36)
    )

    draw.rectangle((360, 235, 445, 360), fill=(30, 33, 50))
    draw.polygon(
        [(350, 240), (402, 160), (455, 240)],
        fill=(18, 21, 36)
    )

    # Glowing windows
    light = (255, 190 + glow, 80)
    for x in (125, 205, 335, 405):
        draw.rounded_rectangle(
            (x, 390, x + 42, 500),
            radius=8,
            fill=light,
            outline=(10, 10, 20),
            width=5
        )
        draw.line(
            (x + 21, 390, x + 21, 500),
            fill=(50, 35, 25),
            width=4
        )
        draw.line(
            (x, 445, x + 42, 445),
            fill=(50, 35, 25),
            width=4
        )

    # Door
    draw.rectangle(
        (225, 545, 315, 710),
        fill=(15, 17, 29),
        outline=(8, 8, 15),
        width=5
    )
    draw.ellipse((295, 620, 305, 630), fill=(255, 190, 60))


def draw_panda(draw, x, y, scale=1.0, step=0):
    s = scale

    # Legs move while walking
    leg_move = math.sin(step) * 15 * s

    draw.line(
        (x - 28*s, y + 65*s, x - 35*s + leg_move, y + 125*s),
        fill=(15, 15, 20),
        width=max(8, int(24*s))
    )
    draw.line(
        (x + 28*s, y + 65*s, x + 35*s - leg_move, y + 125*s),
        fill=(15, 15, 20),
        width=max(8, int(24*s))
    )

    # Body and coat
    draw.ellipse(
        (x - 65*s, y - 5*s, x + 65*s, y + 115*s),
        fill=(130, 82, 43),
        outline=(35, 22, 15),
        width=3
    )

    # Head
    draw.ellipse(
        (x - 65*s, y - 110*s, x + 65*s, y + 20*s),
        fill=(245, 245, 235),
        outline=(20, 20, 25),
        width=4
    )

    # Ears
    draw.ellipse(
        (x - 75*s, y - 120*s, x - 25*s, y - 70*s),
        fill=(15, 15, 20)
    )
    draw.ellipse(
        (x + 25*s, y - 120*s, x + 75*s, y - 70*s),
        fill=(15, 15, 20)
    )

    # Eye patches
    draw.ellipse(
        (x - 48*s, y - 75*s, x - 8*s, y - 25*s),
        fill=(15, 15, 20)
    )
    draw.ellipse(
        (x + 8*s, y - 75*s, x + 48*s, y - 25*s),
        fill=(15, 15, 20)
    )

    # Eyes
    draw.ellipse(
        (x - 30*s, y - 58*s, x - 18*s, y - 43*s),
        fill="white"
    )
    draw.ellipse(
        (x + 18*s, y - 58*s, x + 30*s, y - 43*s),
        fill="white"
    )

    # Nose
    draw.ellipse(
        (x - 9*s, y - 30*s, x + 9*s, y - 17*s),
        fill=(10, 10, 10)
    )

    # Hat
    draw.polygon(
        [
            (x - 65*s, y - 95*s),
            (x - 35*s, y - 145*s),
            (x + 35*s, y - 145*s),
            (x + 65*s, y - 95*s)
        ],
        fill=(100, 62, 35)
    )
    draw.rectangle(
        (x - 78*s, y - 100*s, x + 78*s, y - 88*s),
        fill=(65, 42, 25)
    )

    # Magnifying glass
    mx = x + 70*s
    my = y + 40*s
    draw.ellipse(
        (mx - 20*s, my - 20*s, mx + 20*s, my + 20*s),
        outline=(230, 190, 90),
        width=max(3, int(6*s))
    )
    draw.line(
        (mx + 15*s, my + 15*s, mx + 40*s, my + 45*s),
        fill=(230, 190, 90),
        width=max(3, int(7*s))
    )


def make_frame(frame_number):
    scene = frame_number // (FPS * SCENE_SECONDS)
    local = frame_number % (FPS * SCENE_SECONDS)
    t = local / (FPS * SCENE_SECONDS)

    image = Image.new("RGB", (W, H), (8, 13, 34))
    draw = ImageDraw.Draw(image)

    # Night sky
    for y in range(H):
        shade = int(20 + 20 * y / H)
        draw.line((0, y, W, y), fill=(8, 15, shade))

    # Moon
    moon_x = 420 - int(t * 25)
    draw.ellipse(
        (moon_x - 55, 100, moon_x + 55, 210),
        fill=(240, 225, 175)
    )

    # Mansion
    glow = int(20 * abs(math.sin(frame_number / 12)))
    draw_mansion(draw, glow)

    # Rain
    for i in range(75):
        rx = (i * 83 + frame_number * 9) % W
        ry = (i * 47 + frame_number * 18) % H
        draw.line(
            (rx, ry, rx - 10, ry + 25),
            fill=(105, 145, 190),
            width=2
        )

    # Ground
    draw.rectangle((0, 710, W, H), fill=(15, 20, 32))

    # Scene animations
    if scene == 0:
        panda_x = int(90 + t * 230)
        draw_panda(draw, panda_x, 740, 0.85, frame_number)

    elif scene == 1:
        draw_panda(draw, 270, 740, 1.0, frame_number)

    elif scene == 2:
        draw_panda(draw, 220, 740, 0.9, frame_number)
        # Hidden key
        key_x = 370
        draw.ellipse(
            (key_x, 800, key_x + 35, 835),
            outline=(255, 205, 75),
            width=7
        )
        draw.line(
            (key_x + 30, 820, key_x + 85, 820),
            fill=(255, 205, 75),
            width=8
        )
        draw.line(
            (key_x + 65, 820, key_x + 65, 840),
            fill=(255, 205, 75),
            width=6
        )

    elif scene == 3:
        draw_panda(draw, 210, 740, 1.0, frame_number)
        # Moving shadow
        sx = int(390 - 100 * math.sin(t * math.pi))
        draw.ellipse(
            (sx - 45, 590, sx + 45, 850),
            fill=(3, 4, 12)
        )

    else:
        draw_panda(draw, 270, 740, 1.0, frame_number)

    # Lightning flash
    if scene == 3 and local in (20, 21, 22):
        draw.polygon(
            [(400, 0), (350, 180), (390, 180),
             (330, 330), (440, 145), (400, 145)],
            fill=(230, 235, 255)
        )

    # Cinematic title panel
    draw.rounded_rectangle(
        (22, 35, W - 22, 125),
        radius=18,
        fill=(5, 8, 22)
    )
    draw_text_center(draw, 55, "PANDA DETECTIVE", 30, (255, 205, 90))

    # Scene caption
    draw.rounded_rectangle(
        (20, 825, W - 20, 930),
        radius=18,
        fill=(5, 8, 22)
    )
    draw_text_center(draw, 840, TITLES[scene], 23, (255, 210, 100))
    draw_text_center(draw, 885, SUBTITLES[scene], 15, (235, 235, 245))

    image.save(FRAMES / f"frame_{frame_number:05d}.png")


def make_voice():
    text = " ".join(NARRATION)

    subprocess.run(
        [
            "espeak-ng",
            "-v", "en-us",
            "-s", "145",
            "-p", "45",
            "-w", str(OUT / "voice.wav"),
            text
        ],
        check=True
    )


def make_music():
    # Original simple suspense ambience
    sample_rate = 22050
    duration = SCENE_SECONDS * SCENE_COUNT
    count = sample_rate * duration

    t = np.arange(count) / sample_rate

    music = (
        0.12 * np.sin(2 * np.pi * 55 * t)
        + 0.07 * np.sin(2 * np.pi * 82.4 * t)
        + 0.035 * np.sin(2 * np.pi * 110 * t)
    )

    # Slow fade in and fade out
    fade = np.minimum(1, t / 2)
    fade *= np.minimum(1, (duration - t) / 3)
    music *= fade

    audio = np.int16(np.clip(music, -1, 1) * 32767)

    with wave.open(str(OUT / "music.wav"), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(audio.tobytes())


def build_video():
    print("Rendering animated scenes...")

    for i in range(TOTAL_FRAMES):
        make_frame(i)

        if i % 50 == 0:
            print(f"Rendered {i}/{TOTAL_FRAMES} frames")

    print("Creating video...")

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", str(FRAMES / "frame_%05d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "ultrafast",
            "-crf", "23",
            str(OUT / "silent.mp4")
        ],
        check=True
    )


def add_sound():
    print("Creating English narration...")
    make_voice()

    print("Creating suspense music...")
    make_music()

    print("Mixing audio and video...")

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(OUT / "silent.mp4"),
            "-i", str(OUT / "voice.wav"),
            "-i", str(OUT / "music.wav"),
            "-filter_complex",
            "[1:a]volume=1.0[voice];"
            "[2:a]volume=0.22[music];"
            "[voice][music]amix=inputs=2:duration=longest,"
            "apad[audio]",
            "-map", "0:v:0",
            "-map", "[audio]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            "-movflags", "+faststart",
            str(OUT / "Panda_Detective_Episode_001.mp4")
        ],
        check=True
    )


def main():
    print("PANDA DETECTIVE ANIMATION STUDIO")
    print("Episode 001: The Mystery of the Empty Mansion")

    build_video()
    add_sound()

    print("SUCCESS!")
    print("Your episode is in studio_output/")


if __name__ == "__main__":
    main()
