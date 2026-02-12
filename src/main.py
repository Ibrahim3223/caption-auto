import sys
import argparse
import shutil
import tempfile
from pathlib import Path

from .config import Config
from .channels.loader import load_channel, get_next_pending_topic
from .channels.updater import mark_topic_published
from .content.groq_client import GroqContentGenerator
from .video.pexels_client import PexelsVideoFetcher
from .video.ffmpeg_processor import FFmpegProcessor
from .upload.youtube_auth import build_youtube_service
from .upload.youtube_uploader import YouTubeUploader
from .utils.logger import get_logger

logger = get_logger("main")


def process_channel(channel_file: Path, config: Config) -> bool:
    """Process a single channel: pick topic -> generate content -> produce video -> upload.
    Returns True on success, False on failure.
    """
    channel = load_channel(channel_file)

    topic = get_next_pending_topic(channel)
    if topic is None:
        logger.info(f"[{channel.channel_id}] No pending topics. Skipping.")
        return True

    logger.info(
        f"[{channel.channel_id}] Processing topic #{topic.id}: {topic.title}"
    )

    groq = GroqContentGenerator(config)
    pexels = PexelsVideoFetcher(config)
    ffmpeg = FFmpegProcessor(config)

    work_dir = Path(tempfile.mkdtemp(prefix=f"shorts_{channel.channel_id}_"))

    try:
        # Step 1: Generate hook text and description via Groq
        logger.info(f"[{channel.channel_id}] Generating content with Groq...")
        hook_text = groq.generate_hook_text(topic.title, channel.category)
        description = groq.generate_description(
            topic.title, channel.category, channel.channel_name
        )

        # Step 2: Fetch video from Pexels
        search_query = f"{channel.pexels_search_prefix} {topic.title}"
        logger.info(f"[{channel.channel_id}] Fetching Pexels video...")
        raw_video = pexels.search_and_download(search_query, work_dir)

        # Step 3: Produce the Short with FFmpeg
        output_path = work_dir / "final_short.mp4"
        logger.info(f"[{channel.channel_id}] Producing video with FFmpeg...")
        ffmpeg.produce_short(
            raw_video_path=raw_video,
            hook_text=hook_text,
            music_mood=channel.music_mood,
            output_path=output_path,
        )

        # Step 4: Upload to YouTube
        logger.info(f"[{channel.channel_id}] Uploading to YouTube...")
        yt_service = build_youtube_service()
        uploader = YouTubeUploader(yt_service)

        video_id = uploader.upload(
            video_path=output_path,
            title=topic.title,
            description=description,
            tags=channel.default_tags,
            category_id=channel.youtube_category_id,
        )

        # Step 5: Mark topic as published
        mark_topic_published(channel, topic.id, video_id)
        logger.info(
            f"[{channel.channel_id}] SUCCESS - Topic #{topic.id} "
            f"uploaded as {video_id}"
        )
        return True

    except Exception as e:
        logger.error(
            f"[{channel.channel_id}] FAILED on topic #{topic.id}: {e}",
            exc_info=True,
        )
        return False

    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="YouTube Shorts Pipeline")
    parser.add_argument(
        "--channel",
        required=True,
        help="Path to the channel JSON file (e.g., channels/pet_inner_monologue.json)",
    )
    args = parser.parse_args()

    config = Config()

    if not config.PEXELS_API_KEY:
        logger.error("PEXELS_API_KEY environment variable is not set")
        sys.exit(1)
    if not config.GROQ_API_KEY:
        logger.error("GROQ_API_KEY environment variable is not set")
        sys.exit(1)

    channel_file = Path(args.channel)
    if not channel_file.exists():
        logger.error(f"Channel file not found: {channel_file}")
        sys.exit(1)

    logger.info(f"Processing channel: {channel_file}")
    success = process_channel(channel_file, config)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
