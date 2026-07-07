#!/usr/bin/env python3
"""Create a clean 1-minute research-demo style OPSD-V video.

The visual style is intentionally closer to concise research demo videos:
white background, compact section cards, sparse text, and fast figure/video cuts.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from make_explainer_video import (
    CORAL,
    FPS,
    H,
    INK,
    INK_SOFT,
    LINE,
    TEAL,
    TEAL_DARK,
    W,
    WHITE,
    Clip,
    F_BODY,
    F_BODY_BOLD,
    F_H1,
    F_H2,
    F_MONO,
    F_SMALL,
    F_TITLE,
    Writer,
    add_progress,
    draw_wrapped,
    fit_contain,
    fit_cover,
    text_size,
)

BG = (248, 249, 245)
BLUE = (40, 91, 159)
GREEN = (32, 126, 95)
ORANGE = (210, 111, 69)
DARK = (20, 32, 38)


def clean_canvas() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for x in range(0, W, 64):
        d.line((x, 0, x, H), fill=(238, 241, 234), width=1)
    for y in range(0, H, 64):
        d.line((0, y, W, y), fill=(238, 241, 234), width=1)
    d.rectangle((0, 0, W, 12), fill=TEAL_DARK)
    return img


def pill(draw: ImageDraw.ImageDraw, xy: Tuple[int, int], text: str, fill=TEAL_DARK, fg=WHITE):
    x, y = xy
    tw, th = text_size(draw, text, F_MONO)
    draw.rounded_rectangle((x, y, x + tw + 28, y + th + 16), radius=18, fill=fill)
    draw.text((x + 14, y + 7), text, font=F_MONO, fill=fg)


def heading(img: Image.Image, section: str, title: str, subtitle: str = ""):
    d = ImageDraw.Draw(img)
    pill(d, (84, 58), section.upper(), fill=TEAL_DARK)
    d.text((84, 112), title, font=F_H1, fill=DARK)
    if subtitle:
        draw_wrapped(d, (88, 190), subtitle, F_BODY, INK_SOFT, 1260, 8)


def soft_shadow_card(img: Image.Image, box, radius=26, fill=WHITE, outline=(224, 229, 219)):
    x0, y0, x1, y1 = box
    shadow = Image.new("RGBA", (x1 - x0 + 42, y1 - y0 + 42), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((21, 21, x1 - x0 + 21, y1 - y0 + 21), radius=radius, fill=(16, 35, 45, 32))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    img.paste(shadow, (x0 - 21, y0 - 21), shadow)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def video_card(img: Image.Image, frame: Image.Image, box, label: str, color=TEAL_DARK):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    soft_shadow_card(img, box, radius=22)
    panel = fit_cover(frame, (w, h)).convert("RGBA")
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius=22, fill=255)
    img.paste(panel, (x0, y0), mask)
    d = ImageDraw.Draw(img)
    pill(d, (x0 + 18, y0 + 18), label.upper(), fill=color)


def write_scene(writer: Writer, duration: float, render):
    n = int(duration * FPS)
    for i in range(n):
        img = render(i / FPS, i, n)
        add_progress(img, i, n)
        writer.write(img)


def title_scene(root: Path):
    teaser = fit_cover(Image.open(root / "assets/images/teaser.jpg"), (820, 580))

    def render(_t, i, n):
        img = clean_canvas()
        d = ImageDraw.Draw(img)
        d.text((88, 104), "OPSD-V", font=F_TITLE, fill=DARK)
        draw_wrapped(
            d,
            (94, 230),
            "On-Policy Self-Distillation for Post-Training Few-Step Autoregressive Video Generators",
            F_H1,
            DARK,
            900,
            10,
        )
        d.rounded_rectangle((98, 540, 820, 674), radius=24, fill=(235, 244, 238), outline=(198, 222, 207), width=2)
        draw_wrapped(
            d,
            (132, 570),
            "Train on the states the fast AR generator will actually visit.",
            F_BODY_BOLD,
            TEAL_DARK,
            650,
            8,
        )
        video_card(img, teaser, (1010, 175, 1780, 720), "1-min overview", color=BLUE)
        d.text((104, 810), "No audio · 1080p · 60 seconds", font=F_H2, fill=ORANGE)
        return img

    return render


def problem_scene(root: Path):
    base = Clip(root / "assets/videos/ll-mei-000013-base.mp4", (720, 405), 22.0, 6.0)
    ours = Clip(root / "assets/videos/ll-mei-000013-opsdv.mp4", (720, 405), 22.0, 6.0)

    def render(t, i, n):
        img = clean_canvas()
        heading(
            img,
            "Problem",
            "Few-step AR video generation is fast, but fragile.",
            "Every generated chunk is written back into the KV cache. Small errors become future context.",
        )
        d = ImageDraw.Draw(img)
        cards = [
            ("Fast sampler", "4 denoising steps per chunk"),
            ("Autoregressive cache", "generated history conditions later chunks"),
            ("Long-horizon drift", "visual quality and motion degrade over time"),
        ]
        x = 92
        for k, (h, b) in enumerate(cards):
            soft_shadow_card(img, (x, 330, x + 500, 502), radius=22)
            d.text((x + 30, 358), f"0{k+1}", font=F_MONO, fill=ORANGE)
            d.text((x + 92, 352), h, font=F_H2, fill=DARK)
            draw_wrapped(d, (x + 92, 405), b, F_BODY, INK_SOFT, 360, 6)
            x += 560
        video_card(img, base.at(t, 6.0), (180, 610, 900, 1015), "Base", color=(65, 70, 78))
        video_card(img, ours.at(t, 6.0), (1020, 610, 1740, 1015), "+ OPSD-V", color=GREEN)
        return img

    return render


def figure_scene(root: Path, image_path: str, section: str, title: str, subtitle: str, bullets: Sequence[str]):
    fig = Image.open(root / image_path).convert("RGB")

    def render(_t, i, n):
        img = clean_canvas()
        heading(img, section, title, subtitle)
        d = ImageDraw.Draw(img)
        visual = fit_contain(fig, (1080, 610), fill=WHITE)
        soft_shadow_card(img, (780, 310, 1830, 898), radius=24)
        img.paste(visual, (795, 322))
        y = 345
        for k, text in enumerate(bullets):
            color = [BLUE, GREEN, ORANGE][k % 3]
            d.ellipse((110, y + 2, 158, y + 50), fill=color)
            d.text((127, y + 11), str(k + 1), font=F_MONO, fill=WHITE)
            draw_wrapped(d, (180, y), text, F_BODY_BOLD, DARK, 520, 8)
            y += 148
        return img

    return render


def pair_scene(
    root: Path,
    left_path: str,
    right_path: str,
    section: str,
    title: str,
    subtitle: str,
    left_label: str,
    right_label: str,
    start: float,
    duration: float,
):
    left = Clip(root / left_path, (790, 445), start, duration)
    right = Clip(root / right_path, (790, 445), start, duration)

    def render(t, i, n):
        img = clean_canvas()
        heading(img, section, title, subtitle)
        video_card(img, left.at(t, duration), (130, 350, 920, 795), left_label, color=(65, 70, 78))
        video_card(img, right.at(t, duration), (1000, 350, 1790, 795), right_label, color=GREEN)
        d = ImageDraw.Draw(img)
        d.text((130, 855), "Matched prompt · seed · sampler · attention sink", font=F_H2, fill=INK_SOFT)
        return img

    return render


def results_grid_scene(root: Path):
    clips = [
        ("assets/videos/ll-movie-000115-base.mp4", "assets/videos/ll-movie-000115-opsdv.mp4", "LongLive", 18.0),
        ("assets/videos/sf-mei-000010-base.mp4", "assets/videos/sf-mei-000010-opsdv.mp4", "Self-Forcing", 16.0),
    ]
    loaded = []
    for base, ours, name, start in clips:
        loaded.append((Clip(root / base, (600, 338), start, 7.0), Clip(root / ours, (600, 338), start, 7.0), name))

    def render(t, i, n):
        img = clean_canvas()
        heading(
            img,
            "Results",
            "Continued post-training improves long rollouts.",
            "OPSD-V is applied on top of both LongLive and Self-Forcing without changing the inference sampler.",
        )
        positions = [(210, 330), (1110, 330)]
        for (base, ours, name), (x, y) in zip(loaded, positions):
            d = ImageDraw.Draw(img)
            d.text((x, y - 58), name, font=F_H2, fill=DARK)
            video_card(img, base.at(t, 7.0), (x, y, x + 600, y + 338), "Base", color=(65, 70, 78))
            video_card(img, ours.at(t, 7.0), (x, y + 380, x + 600, y + 718), "+ OPSD-V", color=GREEN)
        return img

    return render


def ablation_scene(root: Path):
    x0 = Clip(root / "assets/videos/ablations/loss-target-train-bridge-x0.mp4", (570, 321), 6.0, 6.0)
    vel = Clip(root / "assets/videos/ablations/loss-target-train-bridge-velocity.mp4", (570, 321), 6.0, 6.0)
    stu = Clip(root / "assets/videos/ablations/trajectory-step056-student.mp4", (570, 321), 0.0, 5.0)
    tea = Clip(root / "assets/videos/ablations/trajectory-step056-teacher.mp4", (570, 321), 0.0, 5.0)

    def render(t, i, n):
        img = clean_canvas()
        heading(
            img,
            "Ablations",
            "Two details matter.",
            "The target should be velocity, and the rollout state must remain student-induced.",
        )
        d = ImageDraw.Draw(img)
        d.text((110, 315), "Prediction target", font=F_H2, fill=DARK)
        video_card(img, x0.at(t, 6.0), (110, 370, 680, 691), "x0 loss", color=(65, 70, 78))
        video_card(img, vel.at(t, 6.0), (710, 370, 1280, 691), "velocity", color=GREEN)
        draw_wrapped(d, (132, 730), "Velocity supervision keeps sharper structure over long rollouts.", F_BODY, INK_SOFT, 1060, 8)

        d.text((110, 830), "Trajectory choice", font=F_H2, fill=DARK)
        video_card(img, stu.at(t, 5.0), (760, 820, 1310, 1030), "student", color=(65, 70, 78))
        video_card(img, tea.at(t, 5.0), (1340, 820, 1890, 1030), "teacher", color=GREEN)
        draw_wrapped(d, (110, 890), "Training on teacher trajectories creates a deployment mismatch and collapses into blur.", F_BODY, INK_SOFT, 580, 8)
        return img

    return render


def closing_scene():
    def render(_t, i, n):
        img = clean_canvas()
        d = ImageDraw.Draw(img)
        d.text((98, 150), "OPSD-V", font=F_TITLE, fill=DARK)
        draw_wrapped(
            d,
            (104, 288),
            "A simple post-training recipe for few-step AR video generators.",
            F_H1,
            DARK,
            1260,
            12,
        )
        items = [
            ("On-policy", "student rollout states"),
            ("Cleaner teacher", "real-video cache history"),
            ("Same sampler", "few-step inference preserved"),
        ]
        x = 120
        for h, b in items:
            soft_shadow_card(img, (x, 590, x + 500, 780), radius=24)
            d.text((x + 32, 626), h, font=F_H2, fill=TEAL_DARK)
            draw_wrapped(d, (x + 32, 682), b, F_BODY, INK_SOFT, 410, 8)
            x += 560
        d.text((120, 895), "Less drift · stronger motion · no inference-time slowdown", font=F_H2, fill=ORANGE)
        return img

    return render


def write_scene(writer: Writer, duration: float, render):
    n = int(duration * FPS)
    for i in range(n):
        img = render(i / FPS, i, n)
        add_progress(img, i, n)
        writer.write(img)


def build(root: Path, output: Path):
    writer = Writer(output)
    try:
        write_scene(writer, 5.0, title_scene(root))
        write_scene(writer, 7.0, problem_scene(root))
        write_scene(
            writer,
            8.0,
            figure_scene(
                root,
                "assets/images/overview.jpg",
                "Observation",
                "Cleaner cache history helps immediately.",
                "A training-free intervention shows that older degraded KV history is a key source of long-video drift.",
                [
                    "Same first generated chunk.",
                    "Same recent generated cache.",
                    "Only older history is replaced by real-video context.",
                ],
            ),
        )
        write_scene(
            writer,
            10.0,
            figure_scene(
                root,
                "assets/images/pipeline.png",
                "Method",
                "Keep the student on-policy; clean up the teacher context.",
                "OPSD-V aligns velocity predictions on the student states that will actually occur at deployment.",
                [
                    "Student rolls out with generated KV cache.",
                    "Teacher uses real-video older history.",
                    "Dense velocity alignment over all denoising steps.",
                ],
            ),
        )
        write_scene(writer, 8.0, results_grid_scene(root))
        write_scene(
            writer,
            7.0,
            pair_scene(
                root,
                "assets/videos/ll-movie-000115-base.mp4",
                "assets/videos/ll-movie-000115-opsdv.mp4",
                "Example",
                "Better sustained dynamics.",
                "OPSD-V improves movement while preserving the original few-step AR inference path.",
                "LongLive",
                "LongLive + OPSD-V",
                start=18.0,
                duration=7.0,
            ),
        )
        write_scene(writer, 9.0, ablation_scene(root))
        write_scene(writer, 6.0, closing_scene())
    finally:
        writer.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path("assets/opsdv_explainer_motive_style_1080p.mp4"))
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    build(root, output)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
