#!/usr/bin/env python3
"""Create a 1080p silent OPSD-V explainer video from project-page assets.

This script intentionally uses only PyAV, Pillow, and NumPy so it can run on the
remote environment where ffmpeg is not available as a shell binary.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


W, H = 1920, 1080
FPS = 24
PAPER = (243, 241, 230)
INK = (24, 55, 47)
INK_SOFT = (83, 107, 98)
TEAL = (47, 125, 92)
TEAL_DARK = (18, 68, 52)
CORAL = (174, 104, 78)
WHITE = (255, 253, 248)
LINE = (204, 211, 194)


def find_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf",
        f"/usr/share/fonts/dejavu/{name}.ttf",
        f"/System/Library/Fonts/Supplemental/{name}.ttf",
        f"/Library/Fonts/{name}.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    fallback = "DejaVuSans-Bold.ttf" if "Bold" in name else "DejaVuSans.ttf"
    return ImageFont.truetype(fallback, size=size)


F_TITLE = find_font("DejaVuSerif-Bold", 86)
F_H1 = find_font("DejaVuSerif-Bold", 58)
F_H2 = find_font("DejaVuSans-Bold", 34)
F_BODY = find_font("DejaVuSans", 30)
F_BODY_BOLD = find_font("DejaVuSans-Bold", 30)
F_SMALL = find_font("DejaVuSans", 23)
F_MONO = find_font("DejaVuSansMono-Bold", 22)


def fit_cover(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    img = img.convert("RGB")
    sw, sh = size
    scale = max(sw / img.width, sh / img.height)
    nw, nh = int(img.width * scale + 0.5), int(img.height * scale + 0.5)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - sw) // 2)
    top = max(0, (nh - sh) // 2)
    return resized.crop((left, top, left + sw, top + sh))


def fit_contain(img: Image.Image, size: Tuple[int, int], fill=WHITE) -> Image.Image:
    img = img.convert("RGB")
    sw, sh = size
    scale = min(sw / img.width, sh / img.height)
    nw, nh = int(img.width * scale + 0.5), int(img.height * scale + 0.5)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    out = Image.new("RGB", size, fill)
    out.paste(resized, ((sw - nw) // 2, (sh - nh) // 2))
    return out


def rounded_rectangle(draw: ImageDraw.ImageDraw, xy, radius: int, fill, outline=None, width: int = 1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
    lines: List[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            candidate = f"{line} {word}"
            if text_size(draw, candidate, font)[0] <= max_width:
                line = candidate
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill,
    max_width: int,
    line_gap: int = 10,
):
    x, y = xy
    for line in wrap_text(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += text_size(draw, line or " ", font)[1] + line_gap
    return y


def base_canvas() -> Image.Image:
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    r = PAPER[0] + 9 * (1 - y) - 8 * x
    g = PAPER[1] + 11 * (1 - y) - 5 * x
    b = PAPER[2] + 15 * (1 - y) + 0 * x
    arr = np.dstack([r, g, b]).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(arr, "RGB")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((-300, -360, 720, 650), fill=(66, 145, 94, 42))
    od.ellipse((1380, 40, 2180, 840), outline=(47, 125, 92, 60), width=3)
    od.ellipse((1500, 180, 2000, 680), outline=(174, 104, 78, 45), width=2)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def add_progress(img: Image.Image, frame_idx: int, total_frames: int) -> None:
    draw = ImageDraw.Draw(img)
    margin = 80
    y = H - 44
    draw.rounded_rectangle((margin, y, W - margin, y + 6), radius=3, fill=(210, 218, 203))
    width = int((W - 2 * margin) * min(1.0, frame_idx / max(1, total_frames - 1)))
    draw.rounded_rectangle((margin, y, margin + width, y + 6), radius=3, fill=TEAL)


def badge(draw: ImageDraw.ImageDraw, xy: Tuple[int, int], text: str, fill=TEAL_DARK):
    x, y = xy
    tw, th = text_size(draw, text, F_MONO)
    draw.rounded_rectangle((x, y, x + tw + 26, y + th + 16), radius=18, fill=fill)
    draw.text((x + 13, y + 7), text, font=F_MONO, fill=WHITE)


def draw_video_panel(
    canvas: Image.Image,
    frame: Image.Image,
    xy: Tuple[int, int],
    size: Tuple[int, int],
    label: str,
    label_fill=TEAL_DARK,
):
    x, y = xy
    w, h = size
    panel = fit_cover(frame, size).convert("RGBA")
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius=24, fill=255)
    shadow = Image.new("RGBA", (w + 36, h + 36), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((18, 18, w + 18, h + 18), radius=24, fill=(20, 46, 57, 45))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    canvas.paste(shadow, (x - 18, y - 18), shadow)
    canvas.paste(panel, (x, y), mask)
    d = ImageDraw.Draw(canvas)
    badge(d, (x + 22, y + 22), label.upper(), fill=label_fill)


def draw_header(img: Image.Image, kicker: str, title: str, subtitle: str | None = None):
    draw = ImageDraw.Draw(img)
    draw.text((86, 58), kicker.upper(), font=F_MONO, fill=TEAL)
    draw.text((84, 88), title, font=F_H1, fill=INK)
    if subtitle:
        draw_wrapped(draw, (88, 164), subtitle, F_BODY, INK_SOFT, 1180, line_gap=8)


class Clip:
    def __init__(self, path: Path, size: Tuple[int, int], start: float, duration: float):
        self.frames = self._load(path, size, start, duration)

    @staticmethod
    def _load(path: Path, size: Tuple[int, int], start: float, duration: float) -> List[Image.Image]:
        container = av.open(str(path))
        stream = container.streams.video[0]
        avg_rate = float(stream.average_rate) if stream.average_rate else 16.0
        out: List[Tuple[float, Image.Image]] = []
        fallback_idx = 0
        end = start + duration + 0.2
        for frame in container.decode(stream):
            t = float(frame.pts * stream.time_base) if frame.pts is not None else fallback_idx / avg_rate
            fallback_idx += 1
            if t < start:
                continue
            if t > end:
                break
            img = fit_cover(frame.to_image(), size)
            out.append((t - start, img))
        container.close()
        if not out:
            raise RuntimeError(f"No frames decoded from {path}")
        images = [img for _, img in out]
        return images

    def at(self, t: float, duration: float) -> Image.Image:
        idx = int((max(0.0, min(duration, t)) / max(0.001, duration)) * (len(self.frames) - 1))
        return self.frames[idx]


class Writer:
    def __init__(self, output: Path):
        output.parent.mkdir(parents=True, exist_ok=True)
        self.container = av.open(str(output), mode="w")
        self.stream = self.container.add_stream("libx264", rate=FPS)
        self.stream.width = W
        self.stream.height = H
        self.stream.pix_fmt = "yuv420p"
        self.stream.options = {"crf": "20", "preset": "medium"}
        self.frame_count = 0

    def write(self, img: Image.Image):
        frame = av.VideoFrame.from_ndarray(np.asarray(img.convert("RGB")), format="rgb24")
        for packet in self.stream.encode(frame):
            self.container.mux(packet)
        self.frame_count += 1

    def close(self):
        for packet in self.stream.encode():
            self.container.mux(packet)
        self.container.close()


def write_static_scene(writer: Writer, duration: float, render):
    n = int(duration * FPS)
    for i in range(n):
        img = render(i / FPS, i, n)
        add_progress(img, i, n)
        writer.write(img)


def write_pair_scene(
    writer: Writer,
    root: Path,
    left_path: str,
    right_path: str,
    duration: float,
    title: str,
    subtitle: str,
    left_label: str,
    right_label: str,
    start: float = 0.0,
):
    panel_size = (830, 467)
    left = Clip(root / left_path, panel_size, start, duration)
    right = Clip(root / right_path, panel_size, start, duration)
    n = int(duration * FPS)
    for i in range(n):
        t = i / FPS
        img = base_canvas()
        draw_header(img, "Comparison", title, subtitle)
        draw_video_panel(img, left.at(t, duration), (90, 300), panel_size, left_label, label_fill=(38, 57, 55))
        draw_video_panel(img, right.at(t, duration), (1000, 300), panel_size, right_label, label_fill=TEAL)
        d = ImageDraw.Draw(img)
        d.line((960, 312, 960, 760), fill=(47, 125, 92, 85), width=3)
        draw_wrapped(d, (116, 815), "Same prompt, seed, sampler, and attention-sink inference setting.", F_SMALL, INK_SOFT, 1660, 6)
        add_progress(img, i, n)
        writer.write(img)


def image_slide(root: Path, image_path: str, title: str, subtitle: str, bullets: Sequence[str], kicker: str = "OPSD-V"):
    src = Image.open(root / image_path).convert("RGB")

    def render(_t, i, n):
        img = base_canvas()
        draw_header(img, kicker, title, subtitle)
        visual = fit_contain(src, (980, 600), fill=WHITE)
        draw_video_panel(img, visual, (850, 300), (980, 600), "Figure", label_fill=TEAL_DARK)
        d = ImageDraw.Draw(img)
        y = 315
        for k, bullet_text in enumerate(bullets, 1):
            d.rounded_rectangle((90, y, 745, y + 112), radius=22, fill=(255, 253, 248), outline=LINE, width=2)
            d.text((120, y + 28), f"0{k}", font=F_MONO, fill=CORAL)
            draw_wrapped(d, (188, y + 22), bullet_text, F_BODY_BOLD if k == 1 else F_BODY, INK, 510, 6)
            y += 132
        add_progress(img, i, n)
        return img

    return render


def title_scene(root: Path):
    bg = Image.open(root / "assets/images/teaser.jpg").convert("RGB")
    bg = fit_cover(bg, (W, H)).filter(ImageFilter.GaussianBlur(2))
    overlay = Image.new("RGBA", (W, H), (8, 28, 22, 142))
    base = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")

    def render(_t, i, n):
        img = base.copy()
        d = ImageDraw.Draw(img)
        d.text((92, 82), "OPSD-V", font=F_TITLE, fill=WHITE)
        draw_wrapped(
            d,
            (98, 198),
            "On-Policy Self-Distillation for Post-Training Few-Step Autoregressive Video Generators",
            F_H1,
            (237, 244, 228),
            1180,
            10,
        )
        d.rounded_rectangle((100, 500, 960, 665), radius=28, fill=(255, 253, 248, 230))
        draw_wrapped(
            d,
            (140, 535),
            "Continue training fast AR video generators on the states they actually visit, while a cleaner teacher corrects long-horizon drift.",
            F_BODY_BOLD,
            INK,
            780,
            8,
        )
        badge(d, (104, 718), "NO VOICE · 1080P · METHOD OVERVIEW", fill=TEAL)
        add_progress(img, i, n)
        return img

    return render


def closing_scene():
    def render(_t, i, n):
        img = base_canvas()
        d = ImageDraw.Draw(img)
        d.text((104, 168), "OPSD-V", font=F_TITLE, fill=INK)
        draw_wrapped(
            d,
            (110, 300),
            "Post-train few-step AR video generators on-policy.",
            F_H1,
            INK,
            1250,
            12,
        )
        cards = [
            ("Student", "rolls out exactly as deployed"),
            ("Teacher", "uses cleaner real-video context"),
            ("Loss", "matches velocity on student states"),
        ]
        x = 110
        for head, body in cards:
            d.rounded_rectangle((x, 548, x + 500, 742), radius=28, fill=WHITE, outline=LINE, width=2)
            d.text((x + 34, 582), head, font=F_H2, fill=TEAL_DARK)
            draw_wrapped(d, (x + 34, 638), body, F_BODY, INK_SOFT, 420, 8)
            x += 545
        d.text((112, 865), "Less drift. Stronger motion. Same few-step inference path.", font=F_H2, fill=CORAL)
        add_progress(img, i, n)
        return img

    return render


def build(root: Path, output: Path):
    writer = Writer(output)
    try:
        write_static_scene(writer, 6.0, title_scene(root))
        write_pair_scene(
            writer,
            root,
            "assets/videos/ll-mei-000013-base.mp4",
            "assets/videos/ll-mei-000013-opsdv.mp4",
            8.0,
            "Long rollouts expose cache-state drift.",
            "Few-step AR generation is fast, but small errors are written back into the KV cache and become future context.",
            "Base",
            "+ OPSD-V",
            start=10.0,
        )
        write_static_scene(
            writer,
            9.0,
            image_slide(
                root,
                "assets/images/overview.jpg",
                "A simple diagnostic reveals the bottleneck.",
                "Replacing older KV-cache history with real-video context improves the rollout even without training.",
                [
                    "The first generated chunk is shared.",
                    "Only older cache history changes.",
                    "Cleaner context reduces long-horizon degradation.",
                ],
                kicker="Motivation",
            ),
        )
        write_static_scene(
            writer,
            14.0,
            image_slide(
                root,
                "assets/images/pipeline.png",
                "Cache-aware on-policy self-distillation.",
                "The student stays on its own inference trajectory; the teacher supplies cleaner corrective targets at the same states.",
                [
                    "Student rollout: generated history in cache.",
                    "Teacher context: real-video older history.",
                    "Dense velocity alignment over every denoising step.",
                ],
                kicker="Method",
            ),
        )
        write_pair_scene(
            writer,
            root,
            "assets/videos/ll-movie-000115-base.mp4",
            "assets/videos/ll-movie-000115-opsdv.mp4",
            8.0,
            "Continued post-training improves dynamics.",
            "On LongLive, OPSD-V preserves the fast sampler while sustaining motion over the full rollout.",
            "LongLive",
            "LongLive + OPSD-V",
            start=18.0,
        )
        write_pair_scene(
            writer,
            root,
            "assets/videos/sf-mei-000010-base.mp4",
            "assets/videos/sf-mei-000010-opsdv.mp4",
            8.0,
            "The same idea transfers to Self-Forcing.",
            "OPSD-V is applied as continued training, not a new inference-time sampler.",
            "Self-Forcing",
            "Self-Forcing + OPSD-V",
            start=16.0,
        )
        write_pair_scene(
            writer,
            root,
            "assets/videos/ablations/loss-target-train-bridge-x0.mp4",
            "assets/videos/ablations/loss-target-train-bridge-velocity.mp4",
            8.0,
            "Ablation: match velocity, not reconstructed x0.",
            "Velocity supervision better preserves fine structure and long-horizon clarity.",
            "x0 loss",
            "Velocity loss",
            start=6.0,
        )
        write_pair_scene(
            writer,
            root,
            "assets/videos/ablations/trajectory-step056-student.mp4",
            "assets/videos/ablations/trajectory-step056-teacher.mp4",
            8.0,
            "Ablation: keep the student trajectory on-policy.",
            "Using teacher trajectories as the rollout target creates a deployment mismatch and collapses into blur.",
            "Student trajectory",
            "Teacher trajectory",
            start=0.0,
        )
        write_static_scene(writer, 5.0, closing_scene())
    finally:
        writer.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path("assets/opsdv_explainer_1080p.mp4"))
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    build(root, output)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
