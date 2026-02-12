import subprocess
import random
from pathlib import Path
from ..config import Config
from .text_wrapper import wrap_hook_text, escape_ffmpeg_text
from ..utils.logger import get_logger

logger = get_logger(__name__)


class FFmpegProcessor:
    def __init__(self, config: Config):
        self.config = config
        self.width = config.VIDEO_WIDTH
        self.height = config.VIDEO_HEIGHT
        self.max_duration = config.VIDEO_MAX_DURATION
        self.fps = config.VIDEO_FPS
        self.hook_font = str(config.FONTS_DIR / config.HOOK_FONT).replace("\\", "/")
        self.cta_font = str(config.FONTS_DIR / config.CTA_FONT).replace("\\", "/")
        self.hook_font_size = config.HOOK_FONT_SIZE
        self.cta_font_size = config.CTA_FONT_SIZE
        self.music_dir = config.MUSIC_DIR

    def produce_short(
        self,
        raw_video_path: Path,
        hook_text: str,
        music_mood: str,
        output_path: Path,
    ) -> Path:
        music_file = self._pick_music(music_mood)
        has_audio = self._has_audio_stream(raw_video_path)
        filter_complex = self._build_filter_complex(hook_text, has_audio)

        cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_video_path),
            "-i", str(music_file),
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "[aout]",
            "-t", str(self.max_duration),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_path),
        ]

        logger.info("Running FFmpeg to produce short...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            logger.error(f"FFmpeg stderr: {result.stderr}")
            raise RuntimeError(
                f"FFmpeg failed with code {result.returncode}: {result.stderr[-500:]}"
            )

        logger.info(f"Produced short: {output_path}")
        return output_path

    def _has_audio_stream(self, video_path: Path) -> bool:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "a",
                "-show_entries", "stream=codec_type",
                "-of", "csv=p=0",
                str(video_path),
            ],
            capture_output=True,
            text=True,
        )
        return "audio" in result.stdout

    def _build_filter_complex(self, hook_text: str, has_audio: bool) -> str:
        w, h = self.width, self.height

        # Step 1: Scale and crop video to portrait
        scale_crop = (
            f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h},fps={self.fps},setsar=1[scaled]"
        )

        # Step 2: Dark overlays for text readability
        # Top region: semi-transparent black behind hook text
        # Bottom region: semi-transparent black behind CTA
        gradient_overlay = (
            f"[scaled]drawbox=x=0:y=0:w={w}:h={int(h * 0.45)}:"
            f"color=black@0.5:t=fill[topdarken];"
            f"[topdarken]drawbox=x=0:y={int(h * 0.70)}:w={w}:h={int(h * 0.30)}:"
            f"color=black@0.4:t=fill[darkened]"
        )

        # Step 3: Hook text overlays (multi-line, with fade-in)
        lines = wrap_hook_text(hook_text)
        hook_filters = self._build_hook_text_filters(lines)

        # Step 4: CTA banner at bottom with arrow
        cta_filter = self._build_cta_banner_filter()

        # Step 5: Audio mixing
        if has_audio:
            audio_mix = (
                f"[0:a]volume=0.3[vorig];"
                f"[1:a]volume=0.15,afade=t=in:st=0:d=1,"
                f"afade=t=out:st={self.max_duration - 1}:d=1[vmusic];"
                f"[vorig][vmusic]amix=inputs=2:duration=shortest[aout]"
            )
        else:
            audio_mix = (
                f"[1:a]volume=0.25,afade=t=in:st=0:d=1,"
                f"afade=t=out:st={self.max_duration - 1}:d=1[aout]"
            )

        parts = [scale_crop, gradient_overlay] + hook_filters + [cta_filter, audio_mix]
        return ";".join(parts)

    def _build_hook_text_filters(self, lines: list[str]) -> list[str]:
        filters = []
        line_height = self.hook_font_size + 20
        start_y = int(self.height * 0.18)
        prev_label = "darkened"

        for i, line in enumerate(lines):
            escaped = escape_ffmpeg_text(line)
            out_label = f"hook{i}"
            y_pos = start_y + (i * line_height)

            # Fade-in: each line appears 0.3s after the previous
            fade_start = 0.2 + (i * 0.3)
            alpha_expr = f"if(lt(t\\,{fade_start})\\,0\\,min(1\\,(t-{fade_start})/0.5))"

            drawtext = (
                f"[{prev_label}]drawtext="
                f"fontfile='{self.hook_font}':"
                f"text='{escaped}':"
                f"fontcolor=white:"
                f"fontsize={self.hook_font_size}:"
                f"alpha='{alpha_expr}':"
                f"borderw=4:"
                f"bordercolor=black@0.8:"
                f"shadowcolor=black@0.7:"
                f"shadowx=3:shadowy=3:"
                f"x=(w-text_w)/2:"
                f"y={y_pos}"
                f"[{out_label}]"
            )
            filters.append(drawtext)
            prev_label = out_label

        # Rename the last label to [hooked] for CTA chaining
        if filters:
            filters[-1] = filters[-1].rsplit("[", 1)[0] + "[hooked]"

        return filters

    def _build_cta_banner_filter(self) -> str:
        # Down arrow + text
        cta_text = escape_ffmpeg_text("READ THE DESCRIPTION \u2B07")
        y_pos = int(self.height * 0.80)
        box_padding = 22

        # CTA fades in after hook text at ~1.5s
        alpha_expr = "if(lt(t\\,1.5)\\,0\\,min(1\\,(t-1.5)/0.4))"

        return (
            f"[hooked]drawtext="
            f"fontfile='{self.cta_font}':"
            f"text='{cta_text}':"
            f"fontcolor=white:"
            f"fontsize={self.cta_font_size}:"
            f"alpha='{alpha_expr}':"
            f"box=1:"
            f"boxcolor=#FF0040@0.9:"
            f"boxborderw={box_padding}:"
            f"borderw=0:"
            f"x=(w-text_w)/2:"
            f"y={y_pos}"
            f"[vout]"
        )

    def _pick_music(self, mood: str) -> Path:
        music_files = list(self.music_dir.glob("*.mp3"))
        if not music_files:
            raise FileNotFoundError(
                f"No music files found in {self.music_dir}. "
                f"Add .mp3 files to assets/music/"
            )
        mood_files = [f for f in music_files if mood in f.stem.lower()]
        pool = mood_files if mood_files else music_files
        return random.choice(pool)
