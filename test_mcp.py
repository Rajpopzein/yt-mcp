import os
import asyncio
from fastapi.testclient import TestClient
from api.index import app, mcp
from api.youtube import normalize_handle

# Initialize FastAPI TestClient
client = TestClient(app)

def test_routes():
    print("Testing HTTP endpoints...")
    
    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "YouTube Channel MCP Server"
    print("[OK] GET / OK")

    # Test Swagger documentation
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower() or "openapi" in response.text.lower()
    print("[OK] GET /docs OK")

def test_normalization():
    print("\nTesting handle normalization...")
    assert normalize_handle("@GoogleDevelopers") == "GoogleDevelopers"
    assert normalize_handle("GoogleDevelopers") == "GoogleDevelopers"
    assert normalize_handle("   @GoogleDevelopers   ") == "GoogleDevelopers"
    print("[OK] Handle normalization OK")

async def test_mcp_tools():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key or api_key == "your_youtube_api_key_here" or api_key.strip() == "":
        print("\nSkipping live YouTube API tool tests because YOUTUBE_API_KEY is not configured in the environment.")
        return

    print("\nTesting MCP tools via FastMCP test client...")
    try:
        # Call get_channel_details
        print("Calling get_channel_details for handle 'GoogleDevelopers'...")
        details_json = await mcp.call_tool("get_channel_details", arguments={"handle": "GoogleDevelopers"})
        print(f"[OK] get_channel_details tool OK.")
        print(f"Details result: {details_json}")

        # Call get_channel_videos
        print("\nCalling get_channel_videos for handle 'GoogleDevelopers'...")
        videos_json = await mcp.call_tool("get_channel_videos", arguments={"handle": "GoogleDevelopers", "limit": 2})
        print(f"[OK] get_channel_videos tool OK.")
        print(f"Videos result: {videos_json}")

        # Call get_video_analytics (New Tool)
        print("\nCalling get_video_analytics for video ID 'bfvS1UeAkN0'...")
        analytics_json = await mcp.call_tool("get_video_analytics", arguments={"video_ids": "bfvS1UeAkN0"})
        print(f"[OK] get_video_analytics tool OK.")
        print(f"Video Analytics result: {analytics_json}")
        
        # FastMCP call_tool returns a tuple (content_list, extra_meta)
        result_str = analytics_json[0][0].text if isinstance(analytics_json, tuple) else analytics_json
        
        import json
        videos_data = json.loads(result_str)
        assert isinstance(videos_data, list)
        if videos_data:
            video = videos_data[0]
            assert "videoId" in video
            assert "title" in video
            assert "statistics" in video
            if os.getenv("YOUTUBE_CLIENT_ID") and os.getenv("YOUTUBE_REFRESH_TOKEN"):
                assert "analytics" in video
                print("[OK] Private analytics verified in get_video_analytics response")

        # Call get_channel_video_analytics (New Tool)
        print("\nCalling get_channel_video_analytics for handle 'GoogleDevelopers'...")
        channel_analytics_json = await mcp.call_tool("get_channel_video_analytics", arguments={"handle": "GoogleDevelopers", "limit": 2})
        print(f"[OK] get_channel_video_analytics tool OK.")
        print(f"Channel Video Analytics result: {channel_analytics_json}")
        
        chan_result_str = channel_analytics_json[0][0].text if isinstance(channel_analytics_json, tuple) else channel_analytics_json
        chan_data = json.loads(chan_result_str)
        assert "videos" in chan_data
        if chan_data["videos"]:
            vid = chan_data["videos"][0]
            assert "videoId" in vid
            if os.getenv("YOUTUBE_CLIENT_ID") and os.getenv("YOUTUBE_REFRESH_TOKEN"):
                assert "analytics" in vid
                print("[OK] Private analytics verified in get_channel_video_analytics response")

    except Exception as e:
        print(f"Tool Test Failed: {e}")
        raise e

async def test_private_analytics_mock():
    print("\nTesting private analytics merging via mock...")
    mock_private_data = {
        "bfvS1UeAkN0": {
            "views": 100,
            "estimatedMinutesWatched": 200,
            "averageViewDuration": 120,
            "averageViewPercentage": 65.5,
            "subscribersGained": 5,
            "subscribersLost": 1,
            "likes": 10,
            "comments": 2,
            "shares": 3,
            "video_thumbnail_impressions": 1000,
            "ctr": 10.0
        }
    }
    
    from unittest.mock import patch, AsyncMock
    with patch("api.youtube.fetch_private_video_analytics", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_private_data
        
        from api.youtube import fetch_video_details
        videos = await fetch_video_details(["bfvS1UeAkN0"])
        
        assert len(videos) == 1
        video = videos[0]
        assert "analytics" in video
        assert video["analytics"]["views"] == 100
        assert video["analytics"]["ctr"] == 10.0
        assert video["analytics"]["averageViewPercentage"] == 65.5
        print("[OK] Private analytics mock merge verified successfully!")

if __name__ == "__main__":
    test_routes()
    test_normalization()
    asyncio.run(test_private_analytics_mock())
    asyncio.run(test_mcp_tools())

