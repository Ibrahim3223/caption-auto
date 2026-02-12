import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ..utils.logger import get_logger

logger = get_logger(__name__)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_URI = "https://oauth2.googleapis.com/token"


def build_youtube_service():
    """Build a YouTube API service from environment variables.

    Expects these env vars (set via GitHub Environment secrets):
        YT_CLIENT_ID
        YT_CLIENT_SECRET
        YT_REFRESH_TOKEN
    """
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        missing = []
        if not client_id:
            missing.append("YT_CLIENT_ID")
        if not client_secret:
            missing.append("YT_CLIENT_SECRET")
        if not refresh_token:
            missing.append("YT_REFRESH_TOKEN")
        raise ValueError(f"Missing YouTube credentials: {', '.join(missing)}")

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=TOKEN_URI,
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )

    service = build("youtube", "v3", credentials=credentials)
    logger.info("Built YouTube service from environment credentials")
    return service
