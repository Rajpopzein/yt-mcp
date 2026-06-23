import os
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from api.config import get_api_key

# Simple in-memory cache for the access token to avoid refreshing on every request
_token_cache = {
    "access_token": None,
    "expires_at": None
}

async def get_oauth2_access_token() -> Optional[str]:
    """
    Retrieves a valid OAuth2 access token by refreshing it if necessary.
    Returns None if client ID, client secret, or refresh token are missing.
    """
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        return None

    # Check if cached token is still valid (with 60 seconds buffer)
    now = datetime.utcnow()
    if _token_cache["access_token"] and _token_cache["expires_at"] and _token_cache["expires_at"] > now + timedelta(seconds=60):
        return _token_cache["access_token"]

    # Refresh the token
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            if response.status_code != 200:
                print(f"Error refreshing OAuth2 token: {response.status_code} - {response.text}")
                return None
            
            token_data = response.json()
            access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 3600)

            if access_token:
                _token_cache["access_token"] = access_token
                _token_cache["expires_at"] = now + timedelta(seconds=expires_in)
                return access_token
    except Exception as e:
        print(f"Exception refreshing OAuth2 token: {str(e)}")
        return None

    return None

async def fetch_private_video_analytics(video_ids: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Fetches private YouTube Analytics API metrics for a list of video IDs.
    Returns a dictionary mapping video ID -> private analytics dictionary.
    """
    if not video_ids:
        return {}

    access_token = await get_oauth2_access_token()
    if not access_token:
        return {}

    start_date = "2005-01-01"
    end_date = datetime.utcnow().strftime("%Y-%m-%d")

    # Full metrics list including impressions and CTR
    metrics_list = [
        "views",
        "estimatedMinutesWatched",
        "averageViewDuration",
        "averageViewPercentage",
        "subscribersGained",
        "subscribersLost",
        "likes",
        "comments",
        "shares",
        "video_thumbnail_impressions",
        "video_thumbnail_impressions_click_rate"
    ]
    
    video_filter = ",".join(video_ids)
    url = "https://youtubeanalytics.googleapis.com/v2/reports"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    async def run_query(query_metrics: List[str]) -> Optional[Dict[str, Dict[str, Any]]]:
        params = {
            "ids": "channel==MINE",
            "startDate": start_date,
            "endDate": end_date,
            "metrics": ",".join(query_metrics),
            "dimensions": "video",
            "filters": f"video=={video_filter}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            if response.status_code != 200:
                print(f"YouTube Analytics API error ({response.status_code}): {response.text}")
                return None

            data = response.json()
            headers_list = data.get("columnHeaders", [])
            col_map = {header["name"]: idx for idx, header in enumerate(headers_list)}
            
            if "video" not in col_map:
                return {}

            video_idx = col_map["video"]
            results = {}
            for row in data.get("rows", []):
                video_id = row[video_idx]
                video_data = {}
                for metric in query_metrics:
                    if metric in col_map:
                        val = row[col_map[metric]]
                        # Convert CTR fractional to percentage
                        if metric == "video_thumbnail_impressions_click_rate":
                            video_data["ctr"] = round(val * 100, 2)
                        elif metric == "averageViewPercentage":
                            video_data["averageViewPercentage"] = round(val, 2)
                        else:
                            video_data[metric] = val
                results[video_id] = video_data
            return results

    try:
        # First attempt with all metrics (including impressions/CTR)
        res = await run_query(metrics_list)
        if res is not None:
            return res
        
        # Fallback list if first query fails (e.g. if channel does not support impressions metrics)
        fallback_metrics = [
            "views",
            "estimatedMinutesWatched",
            "averageViewDuration",
            "averageViewPercentage",
            "subscribersGained",
            "subscribersLost",
            "likes",
            "comments",
            "shares"
        ]
        print("Retrying YouTube Analytics API query with fallback metrics...")
        res = await run_query(fallback_metrics)
        return res if res is not None else {}
    except Exception as e:
        print(f"Exception in fetch_private_video_analytics: {str(e)}")
        return {}


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

async def fetch_video_details(video_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Fetches details and performance statistics for a list of video IDs in batches of up to 50.
    """
    if not video_ids:
        return []
    
    api_key = get_api_key()
    url = 'https://www.googleapis.com/youtube/v3/videos'
    
    # YouTube /videos endpoint only allows up to 50 IDs per request
    chunk_size = 50
    chunks = [video_ids[i:i + chunk_size] for i in range(0, len(video_ids), chunk_size)]
    
    all_videos = []
    
    async with httpx.AsyncClient() as client:
        for chunk in chunks:
            # Join IDs with commas
            ids_param = ",".join([vid.strip() for vid in chunk if vid.strip()])
            if not ids_param:
                continue
                
            params = {
                'part': 'snippet,statistics,contentDetails',
                'id': ids_param,
                'key': api_key
            }
            
            response = await client.get(url, params=params)
            if response.status_code != 200:
                raise Exception(f"YouTube API error ({response.status_code}): {response.text}")
                
            data = response.json()
            items = data.get("items", [])
            
            for item in items:
                snippet = item["snippet"]
                statistics = item.get("statistics", {})
                content_details = item.get("contentDetails", {})
                
                all_videos.append({
                    "videoId": item["id"],
                    "title": snippet["title"],
                    "description": snippet["description"],
                    "publishedAt": snippet["publishedAt"],
                    "url": f"https://www.youtube.com/watch?v={item['id']}",
                    "channelTitle": snippet.get("channelTitle"),
                    "channelId": snippet.get("channelId"),
                    "tags": snippet.get("tags", []),
                    "statistics": {
                        "viewCount": statistics.get("viewCount", "0"),
                        "likeCount": statistics.get("likeCount", "0"),
                        "commentCount": statistics.get("commentCount", "0"),
                        "favoriteCount": statistics.get("favoriteCount", "0"),
                    },
                    "contentDetails": {
                        "duration": content_details.get("duration"),
                        "dimension": content_details.get("dimension"),
                        "definition": content_details.get("definition"),
                        "projection": content_details.get("projection"),
                    }
                })
                
    # Fetch and merge private video analytics if OAuth2 credentials are configured
    if all_videos:
        retrieved_ids = [vid["videoId"] for vid in all_videos]
        private_analytics = await fetch_private_video_analytics(retrieved_ids)
        if private_analytics:
            for video in all_videos:
                vid_id = video["videoId"]
                if vid_id in private_analytics:
                    video["analytics"] = private_analytics[vid_id]
                
    return all_videos

async def fetch_channel_video_analytics(
    channel_id: Optional[str] = None,
    handle: Optional[str] = None,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Fetches the recently uploaded videos of a channel, fully enriched with video statistics.
    """
    # 1. Resolve channel to get uploads playlist ID
    details = await fetch_channel_details(channel_id=channel_id, handle=handle)
    
    # 2. Fetch basic videos from the uploads playlist
    basic_videos = await fetch_channel_videos(details["uploadsPlaylistId"], limit=limit)
    if not basic_videos:
        return {
            "channelTitle": details["title"],
            "channelId": details["id"],
            "videos": []
        }
        
    # 3. Extract video IDs
    video_ids = [vid["videoId"] for vid in basic_videos]
    
    # 4. Fetch enriched details for all video IDs in a batch
    enriched_videos = await fetch_video_details(video_ids)
    
    # Sort the enriched videos to match the order returned by the playlist (newest first)
    video_order = {vid_id: i for i, vid_id in enumerate(video_ids)}
    enriched_videos.sort(key=lambda x: video_order.get(x["videoId"], 999))
    
    return {
        "channelTitle": details["title"],
        "channelId": details["id"],
        "videos": enriched_videos
    }
