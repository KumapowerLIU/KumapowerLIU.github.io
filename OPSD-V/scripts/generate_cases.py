#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path


ROOT = Path("/mnt/dolphinfs/ssd_pool/docker/user/hadoop-videogen-hl/hadoop-camera3d/hongyuliu")
OUTPUT = ROOT / "LongLive-main/output"
SITE = ROOT / "OPSF-V/projectpage"

PROMPT_FILES = {
    "MeiBench": ROOT / "dataset_longvideo_all/holdout_prompts_20_per_root.txt",
    "MovieGenBench": ROOT / "LongLive-main/example/MovieGenVideoBench_extended.txt",
}

GROUPS = [
    {
        "backbone": "LongLive",
        "benchmark": "MeiBench",
        "prefix": "ll-mei",
        "base": OUTPUT / "meibench120_longlive_pps/seed_1",
        "ours": OUTPUT / "meibench120_longlive_nofuture_lora_200step_vloss_pps/seed_1",
        "quality": [3, 7, 9, 13, 16, 19, 57, 83, 97, 106],
        "dynamics": [22, 55, 75, 76, 94, 115],
        "both": [40],
    },
    {
        "backbone": "LongLive",
        "benchmark": "MovieGenBench",
        "prefix": "ll-movie",
        "base": OUTPUT / "moviebench120_longlive_pps/seed_1",
        "ours": OUTPUT / "moviebench120_longlive_nofuture_lora_200step_pps_vloss/seed_1",
        "quality": [3, 9, 19, 33, 40, 62, 87, 89, 100],
        "dynamics": [4, 21, 29, 42, 68, 71, 115],
        "both": [23],
    },
    {
        "backbone": "Self-Forcing",
        "benchmark": "MeiBench",
        "prefix": "sf-mei",
        "base": OUTPUT / "meibench120_sf_pps/seed_1",
        "ours": OUTPUT / "meibench120_sf_pps_lora_vloss/seed_1",
        "quality": [2, 7, 9, 10, 12, 19, 20, 25, 28, 34, 40, 47, 49, 52, 57, 58, 65, 84, 99, 106, 115],
        "dynamics": [54, 69],
        "both": [55, 75, 78, 95, 111],
    },
    {
        "backbone": "Self-Forcing",
        "benchmark": "MovieGenBench",
        "prefix": "sf-movie",
        "base": OUTPUT / "moviebench120_sf_pps/seed_1",
        "ours": OUTPUT / "moviebench120_sf_pps_lora_vloss/seed_1",
        "quality": [23, 70, 76, 87, 94, 102, 105, 109],
        "dynamics": [4, 6],
        "both": [0, 2, 3, 11, 20, 36, 40, 46, 58, 59, 60, 64],
    },
]

TITLE_OVERRIDES = {
    ("LongLive", "MeiBench", 13): "Aerial Great Wall",
    ("LongLive", "MeiBench", 55): "Running by the Coast",
    ("LongLive", "MeiBench", 40): "Antelope in Arid Terrain",
    ("LongLive", "MovieGenBench", 9): "California Gold Rush",
    ("LongLive", "MovieGenBench", 68): "Rabbit Reading the News",
    ("LongLive", "MovieGenBench", 23): "Orangutan Family",
    ("Self-Forcing", "MeiBench", 10): "Tree-Lined Park",
    ("Self-Forcing", "MeiBench", 69): "Home Workout",
    ("Self-Forcing", "MeiBench", 55): "Sunset Coast",
    ("Self-Forcing", "MovieGenBench", 76): "Underwater Tunnel",
    ("Self-Forcing", "MovieGenBench", 4): "Monster and Candle",
    ("Self-Forcing", "MovieGenBench", 40): "Surfing Otter",
}

FEATURED = set(TITLE_OVERRIDES)


def load_prompts():
    return {
        name: path.read_text(encoding="utf-8").splitlines()
        for name, path in PROMPT_FILES.items()
    }


def find_video(directory, case_id):
    matches = sorted(directory.glob(f"{case_id:06d}_*.mp4"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one video for {directory}/{case_id:06d}, found {len(matches)}")
    return matches[0]


def make_title(prompt):
    text = prompt.strip()
    prefixes = [
        "The video shows ",
        "The video displays ",
        "The video depicts ",
        "The scene shows ",
        "A video of ",
        "A video shows ",
    ]
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):]
            break
    text = text.split(".", 1)[0].split(",", 1)[0]
    words = text.split()
    if words and words[0].lower() in {"a", "an", "the"}:
        words = words[1:]
    title = " ".join(words[:7]).strip()
    if len(words) > 7:
        title += "..."
    return title[:1].upper() + title[1:]


def symlink_video(source, destination):
    if destination.is_symlink() or destination.exists():
        destination.unlink()
    destination.symlink_to(source)


def render_poster(video, poster):
    if poster.exists() and poster.stat().st_mtime >= video.stat().st_mtime:
        return
    subprocess.run(
        [
            "ffmpeg", "-nostdin", "-y", "-loglevel", "error",
            "-ss", "30", "-i", str(video), "-frames:v", "1",
            "-vf", "scale=832:-2", "-q:v", "3", str(poster),
        ],
        check=True,
    )


def main():
    prompts = load_prompts()
    video_dir = SITE / "assets/videos"
    poster_dir = SITE / "assets/posters"
    video_dir.mkdir(parents=True, exist_ok=True)
    poster_dir.mkdir(parents=True, exist_ok=True)
    cases = []

    for group in GROUPS:
        benchmark_prompts = prompts[group["benchmark"]]
        for category in ("quality", "dynamics", "both"):
            for case_id in group[category]:
                prompt = benchmark_prompts[case_id]
                slug = f"{group['prefix']}-{case_id:06d}"
                base_video = find_video(group["base"], case_id)
                ours_video = find_video(group["ours"], case_id)
                base_link = video_dir / f"{slug}-base.mp4"
                ours_link = video_dir / f"{slug}-opsdv.mp4"
                base_poster = poster_dir / f"{slug}-base.jpg"
                ours_poster = poster_dir / f"{slug}-opsdv.jpg"

                symlink_video(base_video, base_link)
                symlink_video(ours_video, ours_link)
                render_poster(base_video, base_poster)
                render_poster(ours_video, ours_poster)

                key = (group["backbone"], group["benchmark"], case_id)
                cases.append({
                    "slug": slug,
                    "id": f"{case_id:06d}",
                    "title": TITLE_OVERRIDES.get(key, make_title(prompt)),
                    "backbone": group["backbone"],
                    "benchmark": group["benchmark"],
                    "category": category,
                    "featured": key in FEATURED,
                    "prompt": prompt,
                    "baseVideo": f"assets/videos/{slug}-base.mp4",
                    "oursVideo": f"assets/videos/{slug}-opsdv.mp4",
                    "basePoster": f"assets/posters/{slug}-base.jpg",
                    "oursPoster": f"assets/posters/{slug}-opsdv.jpg",
                })

    cases.sort(key=lambda item: (not item["featured"], item["backbone"], item["benchmark"], item["category"], item["id"]))
    output = "export const cases = " + json.dumps(cases, ensure_ascii=False, indent=2) + ";\n"
    (SITE / "cases.generated.js").write_text(output, encoding="utf-8")
    print(f"Generated {len(cases)} cases, {len(cases) * 2} video links, and {len(cases) * 2} posters.")


if __name__ == "__main__":
    main()
