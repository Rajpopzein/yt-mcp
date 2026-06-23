## 1. YouTube API Client Enhancements

- [x] 1.1 Add fetch_video_details function in api/youtube.py supporting batch lookup of up to 50 video IDs
- [x] 1.2 Implement helper to fetch a channel's videos enriched with full video performance metrics
- [x] 1.3 Implement `get_oauth2_access_token()` to refresh and cache access tokens using credentials from the environment
- [x] 1.4 Implement `fetch_private_video_analytics(video_ids)` to call the YouTube Analytics API and query video-level reports
- [x] 1.5 Update `fetch_video_details()` and `fetch_channel_video_analytics()` to fetch private analytics and merge them into the final video objects

## 2. MCP Tool Registrations

- [x] 2.1 Define and register get_video_analytics tool in api/index.py
- [x] 2.2 Define and register get_channel_video_analytics tool in api/index.py
- [x] 2.3 Bind tools to the new async client implementation functions

## 3. Testing and Verification

- [x] 3.1 Update `test_mcp.py` to verify that the private `analytics` block is present in returned video details when credentials are simulated/present
- [x] 3.2 Verify all tests pass successfully


