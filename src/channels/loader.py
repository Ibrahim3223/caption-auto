import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Topic:
    id: int
    title: str
    status: str  # "pending" | "published"
    published_date: Optional[str] = None
    video_id: Optional[str] = None


@dataclass
class Channel:
    channel_id: str
    channel_name: str
    github_environment: str
    category: str
    youtube_category_id: str
    default_tags: list[str]
    pexels_search_prefix: str
    music_mood: str
    topics: list[Topic]
    file_path: Path = field(default_factory=lambda: Path("."))


def load_all_channels(channels_dir: Path) -> list[Channel]:
    channels = []
    for json_file in sorted(channels_dir.glob("*.json")):
        channel = load_channel(json_file)
        channels.append(channel)
    return channels


def load_channel(file_path: Path) -> Channel:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    topics = [
        Topic(
            id=t["id"],
            title=t["title"],
            status=t["status"],
            published_date=t.get("published_date"),
            video_id=t.get("video_id"),
        )
        for t in data["topics"]
    ]

    return Channel(
        channel_id=data["channel_id"],
        channel_name=data["channel_name"],
        github_environment=data["github_environment"],
        category=data["category"],
        youtube_category_id=data["youtube_category_id"],
        default_tags=data["default_tags"],
        pexels_search_prefix=data.get("pexels_search_prefix", ""),
        music_mood=data.get("music_mood", "upbeat"),
        topics=topics,
        file_path=file_path,
    )


def get_next_pending_topic(channel: Channel) -> Optional[Topic]:
    for topic in channel.topics:
        if topic.status == "pending":
            return topic
    return None
