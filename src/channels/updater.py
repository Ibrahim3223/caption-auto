import json
from datetime import datetime, timezone
from .loader import Channel


def mark_topic_published(
    channel: Channel,
    topic_id: int,
    video_id: str,
) -> None:
    with open(channel.file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for topic in data["topics"]:
        if topic["id"] == topic_id:
            topic["status"] = "published"
            topic["published_date"] = datetime.now(timezone.utc).isoformat()
            topic["video_id"] = video_id
            break

    with open(channel.file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
