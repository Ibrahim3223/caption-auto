import textwrap


def wrap_hook_text(
    text: str,
    max_chars_per_line: int = 18,
    max_lines: int = 3,
) -> list[str]:
    """Wrap hook text into lines for FFmpeg drawtext overlay.

    At 72px font size on 1080px width with ~60px padding each side,
    approximately 18 uppercase characters fit per line.
    """
    text = text.upper()
    lines = textwrap.wrap(text, width=max_chars_per_line)
    return lines[:max_lines]


def escape_ffmpeg_text(text: str) -> str:
    """Escape special characters for FFmpeg drawtext filter."""
    text = text.replace("\\", "\\\\")
    text = text.replace(":", "\\:")
    text = text.replace("'", "\\'")
    text = text.replace("%", "%%")
    text = text.replace('"', '\\"')
    return text
