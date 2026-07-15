from __future__ import annotations

import httpx


class DownloadError(RuntimeError):
    pass


def download_subscription(url: str, user_agent: str = "SubBridge/0.1") -> str:
    try:
        response = httpx.get(
            url,
            headers={"User-Agent": user_agent},
            follow_redirects=True,
            timeout=30.0,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise DownloadError(f"Failed to download subscription: {exc}") from exc

    return response.text
