import random
import requests
from pathlib import Path
from ..config import Config
from ..utils.logger import get_logger
from ..utils.retry import retry_with_backoff

logger = get_logger(__name__)


class PexelsVideoFetcher:
    BASE_URL = "https://api.pexels.com/videos/search"

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({"Authorization": config.PEXELS_API_KEY})

    @retry_with_backoff(max_retries=3, base_delay=2.0)
    def search_and_download(self, query: str, output_dir: Path) -> Path:
        params = {
            "query": query,
            "orientation": self.config.PEXELS_VIDEO_ORIENTATION,
            "size": self.config.PEXELS_VIDEO_SIZE,
            "per_page": 15,
            "page": 1,
        }

        logger.info(f"Searching Pexels: {query}")
        response = self.session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        videos = data.get("videos", [])
        if not videos:
            raise ValueError(f"No Pexels videos found for query: {query}")

        # Prefer videos within our duration range
        suitable = [
            v for v in videos
            if self.config.PEXELS_VIDEO_MIN_DURATION
            <= v["duration"]
            <= self.config.PEXELS_VIDEO_MAX_DURATION
        ]
        if not suitable:
            suitable = videos

        # Pick randomly from top results for variety
        chosen = random.choice(suitable[:5])
        video_file = self._select_best_file(chosen["video_files"])

        # Download the video
        output_path = output_dir / f"pexels_{chosen['id']}.mp4"
        self._download_file(video_file["link"], output_path)

        logger.info(
            f"Downloaded Pexels video {chosen['id']} "
            f"({chosen['duration']}s) -> {output_path}"
        )
        return output_path

    def _select_best_file(self, video_files: list[dict]) -> dict:
        # Prefer portrait (height > width) and high resolution
        portrait_files = [
            f for f in video_files
            if f.get("height", 0) > f.get("width", 0)
            and f.get("height", 0) >= 1080
        ]
        if portrait_files:
            return max(portrait_files, key=lambda f: f.get("height", 0))

        # Fallback: any file, prefer highest resolution
        return max(video_files, key=lambda f: f.get("height", 0))

    def _download_file(self, url: str, output_path: Path) -> None:
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
