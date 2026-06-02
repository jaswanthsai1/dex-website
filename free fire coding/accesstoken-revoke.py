#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║           GARENA ACCESS TOKEN REVOKER SCRIPT                ║
║  Prompts for access token, refresh token (optional),        ║
║  and app ID (default 100067)                                ║
╚══════════════════════════════════════════════════════════════╝
"""

import requests

DEFAULT_APP_ID = "100067"
BASE_URL = "https://100067.connect.garena.com/oauth/logout"
USER_AGENT = (
    "GarenaMSDK/4.0.41(DN2101 ;Android 13;en;HK;app 2.123.1 2019117599;)"
)

def revoke_token(access_token, refresh_token=None, app_id=DEFAULT_APP_ID):
    """Send logout request to revoke token."""
    params = {
        "access_token": access_token.strip(),
        "app_id": app_id.strip()
    }
    if refresh_token and refresh_token.strip():
        params["refresh_token"] = refresh_token.strip()

    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    print("\n⏳ Sending revocation request...")
    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        print(f"HTTP Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Token successfully revoked (logout successful).")
            if response.text:
                print(f"Response body: {response.text}")
        else:
            print(f"❌ Revocation failed. Server returned: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")

def main():
    print("=" * 60)
    print("GARENA TOKEN REVOKER")
    print("=" * 60)

    # Prompt for access token
    access_token = input("🔑 Enter access token: ").strip()
    if not access_token:
        print("❌ Access token is required. Exiting.")
        return

    # Prompt for refresh token (optional)
    refresh_token = input("🔄 Enter refresh token (optional, press Enter to skip): ").strip()

    # Prompt for app ID with default
    app_id_input = input(f"📱 Enter app ID (default: {DEFAULT_APP_ID}): ").strip()
    app_id = app_id_input if app_id_input else DEFAULT_APP_ID

    print("-" * 60)
    print(f"Access token : {access_token[:20]}..." if len(access_token) > 20 else f"Access token : {access_token}")
    if refresh_token:
        print(f"Refresh token: {refresh_token[:20]}...")
    print(f"App ID       : {app_id}")
    print(f"Endpoint     : {BASE_URL}")
    print("-" * 60)

    revoke_token(access_token, refresh_token, app_id)

if __name__ == "__main__":
    main()