import http.client
import random
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from ..utils.logger import get_logger

logger = get_logger(__name__)

MAX_RETRIES = 5
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


class YouTubeUploader:
    def __init__(self, service):
        self.service = service

    def upload(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: list[str],
        category_id: str = "22",
    ) -> str:
        """Upload a video to YouTube as a Short. Returns the video ID."""
        if "#Shorts" not in title:
            title = f"{title} #Shorts"

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        }

        media = MediaFileUpload(
            str(video_path),
            mimetype="video/mp4",
            resumable=True,
            chunksize=256 * 1024,
        )

        request = self.service.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )

        logger.info(f"Uploading: {title}")
        return self._resumable_upload(request)

    def _resumable_upload(self, request) -> str:
        response = None
        retry = 0

        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    logger.info(
                        f"Upload progress: {int(status.progress() * 100)}%"
                    )
            except HttpError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    retry += 1
                    if retry > MAX_RETRIES:
                        raise
                    sleep_seconds = 2 ** retry + random.random()
                    logger.warning(
                        f"HTTP {e.resp.status}, retrying in {sleep_seconds:.1f}s "
                        f"(attempt {retry}/{MAX_RETRIES})"
                    )
                    time.sleep(sleep_seconds)
                else:
                    raise
            except (http.client.HTTPException, ConnectionError) as e:
                retry += 1
                if retry > MAX_RETRIES:
                    raise
                sleep_seconds = 2 ** retry + random.random()
                logger.warning(
                    f"Connection error: {e}, retrying in {sleep_seconds:.1f}s"
                )
                time.sleep(sleep_seconds)

        video_id = response["id"]
        logger.info(f"Upload complete. Video ID: {video_id}")
        return video_id
