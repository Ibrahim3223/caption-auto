"""
Interactive script to obtain OAuth2 refresh tokens for YouTube channels.

Usage:
    python scripts/obtain_refresh_token.py

Prerequisites:
    1. Create a Google Cloud project at https://console.cloud.google.com
    2. Enable the YouTube Data API v3
    3. Create OAuth2 credentials (Desktop application type)
    4. Download the client_secret.json file

This script will:
    1. Ask for your client_id and client_secret
    2. Open a browser for OAuth2 authorization
    3. Print the refresh_token to add to your GitHub Secrets
"""

import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    print("=" * 60)
    print("YouTube OAuth2 Refresh Token Generator")
    print("=" * 60)
    print()

    channel_id = input("Enter channel_id (e.g., animal_facts): ").strip()
    client_id = input("Enter OAuth2 Client ID: ").strip()
    client_secret = input("Enter OAuth2 Client Secret: ").strip()

    # Build client config
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    print("\nOpening browser for authorization...")
    print("Please sign in with the Google account that owns this YouTube channel.\n")

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    credentials = flow.run_local_server(port=8080)

    refresh_token = credentials.refresh_token

    print("\n" + "=" * 60)
    print("SUCCESS! Here are your credentials:")
    print("=" * 60)

    creds_json = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }

    print(f"\nChannel ID: {channel_id}")
    print(f"\nAdd this to your YT_CREDENTIALS_STORE secret:")
    print(f'  "{channel_id}": {json.dumps(creds_json)}')
    print()
    print("Full JSON entry:")
    print(json.dumps(creds_json, indent=2))
    print()


if __name__ == "__main__":
    main()
