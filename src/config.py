import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Config:
    # Paths
    PROJECT_ROOT: Path = field(default_factory=lambda: Path(__file__).parent.parent)

    @property
    def CHANNELS_DIR(self) -> Path:
        return self.PROJECT_ROOT / "channels"

    @property
    def ASSETS_DIR(self) -> Path:
        return self.PROJECT_ROOT / "assets"

    @property
    def MUSIC_DIR(self) -> Path:
        return self.ASSETS_DIR / "music"

    @property
    def FONTS_DIR(self) -> Path:
        return self.ASSETS_DIR / "fonts"

    @property
    def OUTPUT_DIR(self) -> Path:
        return self.PROJECT_ROOT / "output"

    # API Keys
    @property
    def PEXELS_API_KEY(self) -> str:
        return os.environ.get("PEXELS_API_KEY", "")

    @property
    def GROQ_API_KEY(self) -> str:
        return os.environ.get("GROQ_API_KEY", "")

    # Pexels settings
    PEXELS_VIDEO_ORIENTATION: str = "portrait"
    PEXELS_VIDEO_MIN_DURATION: int = 5
    PEXELS_VIDEO_MAX_DURATION: int = 15
    PEXELS_VIDEO_SIZE: str = "medium"

    # Video output settings
    VIDEO_WIDTH: int = 1080
    VIDEO_HEIGHT: int = 1920
    VIDEO_MAX_DURATION: int = 10
    VIDEO_FPS: int = 30

    # Font settings
    HOOK_FONT: str = "Montserrat-Bold.ttf"
    CTA_FONT: str = "Montserrat-ExtraBold.ttf"
    HOOK_FONT_SIZE: int = 72
    CTA_FONT_SIZE: int = 52

    # Groq settings
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_MAX_TOKENS_HOOK: int = 60
    GROQ_MAX_TOKENS_DESCRIPTION: int = 1500

    # Rate limiting
    PEXELS_REQUESTS_PER_HOUR: int = 200
