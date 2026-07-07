#!/usr/bin/env bash
set -euo pipefail

ROOT="/mnt/dolphinfs/ssd_pool/docker/user/hadoop-videogen-hl/hadoop-camera3d/hongyuliu"
OUTPUT="$ROOT/LongLive-main/output"
SITE="$ROOT/opsd-v/projectpage"

mkdir -p "$SITE/assets/videos" "$SITE/assets/posters"

add_case() {
  local slug="$1"
  local base_dir="$2"
  local ours_dir="$3"
  local case_id="$4"
  local base_file
  local ours_file

  base_file=$(find "$base_dir" -maxdepth 1 -type f -name "${case_id}_*.mp4" | head -1)
  ours_file=$(find "$ours_dir" -maxdepth 1 -type f -name "${case_id}_*.mp4" | head -1)

  if [[ -z "$base_file" || -z "$ours_file" ]]; then
    echo "Missing pair for $slug ($case_id)" >&2
    return 1
  fi

  ln -sfn "$base_file" "$SITE/assets/videos/${slug}-base.mp4"
  ln -sfn "$ours_file" "$SITE/assets/videos/${slug}-opsdv.mp4"

  ffmpeg -nostdin -y -loglevel error -ss 30 -i "$base_file" \
    -frames:v 1 -vf "scale=832:-2" -q:v 3 "$SITE/assets/posters/${slug}-base.jpg"
  ffmpeg -nostdin -y -loglevel error -ss 30 -i "$ours_file" \
    -frames:v 1 -vf "scale=832:-2" -q:v 3 "$SITE/assets/posters/${slug}-opsdv.jpg"

  printf "prepared %-30s %s\n" "$slug" "$case_id"
}

LL_MEI_BASE="$OUTPUT/meibench120_longlive_pps/seed_1"
LL_MEI_OPSD="$OUTPUT/meibench120_longlive_nofuture_lora_200step_vloss_pps/seed_1"
LL_MOVIE_BASE="$OUTPUT/moviebench120_longlive_pps/seed_1"
LL_MOVIE_OPSD="$OUTPUT/moviebench120_longlive_nofuture_lora_200step_pps_vloss/seed_1"
SF_MEI_BASE="$OUTPUT/meibench120_sf_pps/seed_1"
SF_MEI_OPSD="$OUTPUT/meibench120_sf_pps_lora_vloss/seed_1"
SF_MOVIE_BASE="$OUTPUT/moviebench120_sf_pps/seed_1"
SF_MOVIE_OPSD="$OUTPUT/moviebench120_sf_pps_lora_vloss/seed_1"

add_case "ll-mei-great-wall" "$LL_MEI_BASE" "$LL_MEI_OPSD" "000013"
add_case "ll-mei-coastal-run" "$LL_MEI_BASE" "$LL_MEI_OPSD" "000055"
add_case "ll-mei-antelope" "$LL_MEI_BASE" "$LL_MEI_OPSD" "000040"
add_case "ll-movie-gold-rush" "$LL_MOVIE_BASE" "$LL_MOVIE_OPSD" "000009"
add_case "ll-movie-rabbit-reader" "$LL_MOVIE_BASE" "$LL_MOVIE_OPSD" "000068"
add_case "ll-movie-orangutan-family" "$LL_MOVIE_BASE" "$LL_MOVIE_OPSD" "000023"
add_case "sf-mei-tree-lined-park" "$SF_MEI_BASE" "$SF_MEI_OPSD" "000010"
add_case "sf-mei-home-workout" "$SF_MEI_BASE" "$SF_MEI_OPSD" "000069"
add_case "sf-mei-sunset-coast" "$SF_MEI_BASE" "$SF_MEI_OPSD" "000055"
add_case "sf-movie-underwater-tunnel" "$SF_MOVIE_BASE" "$SF_MOVIE_OPSD" "000076"
add_case "sf-movie-candle-monster" "$SF_MOVIE_BASE" "$SF_MOVIE_OPSD" "000004"
add_case "sf-movie-surfing-otter" "$SF_MOVIE_BASE" "$SF_MOVIE_OPSD" "000040"

echo "Video files: $(find "$SITE/assets/videos" -maxdepth 1 \( -type f -o -type l \) -name '*.mp4' | wc -l)"
echo "Posters:     $(find "$SITE/assets/posters" -maxdepth 1 -type f -name '*.jpg' | wc -l)"
