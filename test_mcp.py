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

        # Call get_channel_video_analytics (New Tool)
        print("\nCalling get_channel_video_analytics for handle 'GoogleDevelopers'...")
        channel_analytics_json = await mcp.call_tool("get_channel_video_analytics", arguments={"handle": "GoogleDevelopers", "limit": 2})
        print(f"[OK] get_channel_video_analytics tool OK.")
        print(f"Channel Video Analytics result: {channel_analytics_json}")

    except Exception as e:
        print(f"Tool Test Failed: {e}")

if __name__ == "__main__":
    test_routes()
    test_normalization()
    asyncio.run(test_mcp_tools())
