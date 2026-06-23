import httpx
from typing import Dict, Any, List, Optional
from api.config import get_api_key

def normalize_handle(handle: str) -> str:
    """
    Normalizes user handle input by removing leading '@' if present.
    """
    h = handle.strip()
    if h.startswith('@'):
        h = h[1:]
    return h

async def fetch_channel_details(channel_id: Optional[str] = None, handle: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetches YouTube channel statistics and metadata by channel ID or handle.
    """
    api_key = get_api_key()
    url = 'https://www.googleapis.com/youtube/v3/channels'
    
    params = {
        'part': 'snippet,statistics,contentDetails',
        'key': api_key
    }
    
    if channel_id:
        params['id'] = channel_id.strip()
    elif handle:
        params['forHandle'] = normalize_handle(handle)
    else:
        raise ValueError("Must provide either channel_id or handle.")

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"YouTube API error ({response.status_code}): {response.text}")

        data = response.json()
        if not data.get("items") or len(data["items"]) == 0:
            identifier = channel_id or handle
            raise ValueError(f"No channel found for identifier: {identifier}")

        item = data["items"][0]
        snippet = item["snippet"]
        statistics = item["statistics"]
        content_details = item["contentDetails"]

        return {
            "id": item["id"],
            "title": snippet["title"],
            "description": snippet["description"],
            "customUrl": snippet.get("customUrl"),
            "publishedAt": snippet["publishedAt"],
            "statistics": {
                "viewCount": statistics.get("viewCount", "0"),
                "subscriberCount": statistics.get("subscriberCount", "0"),
                "hiddenSubscriberCount": statistics.get("hiddenSubscriberCount", False),
                "videoCount": statistics.get("videoCount", "0"),
            },
            "uploadsPlaylistId": content_details["relatedPlaylists"]["uploads"]
        }

async def fetch_channel_videos(uploads_playlist_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Fetches recent video uploads for a channel using its uploads playlist ID.
    """
    api_key = get_api_key()
    url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    
    max_results = min(max(limit, 1), 50)  # Clamp limit between 1 and 50
    params = {
        'part': 'snippet',
        'playlistId': uploads_playlist_id,
        'maxResults': max_results,
        'key': api_key
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"YouTube API error ({response.status_code}): {response.text}")

        data = response.json()
        items = data.get("items", [])

        videos = []
        for item in items:
            snippet = item["snippet"]
            video_id = snippet["resourceId"]["videoId"]
            videos.append({
                "videoId": video_id,
                "title": snippet["title"],
                "description": snippet["description"],
                "publishedAt": snippet["publishedAt"],
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })
        return videos
