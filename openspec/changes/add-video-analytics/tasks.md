## 1. YouTube API Client Enhancements

- [x] 1.1 Add fetch_video_details function in api/youtube.py supporting batch lookup of up to 50 video IDs
- [x] 1.2 Implement helper to fetch a channel's videos enriched with full video performance metrics

## 2. MCP Tool Registrations

- [x] 2.1 Define and register get_video_analytics tool in api/index.py
- [x] 2.2 Define and register get_channel_video_analytics tool in api/index.py
- [x] 2.3 Bind tools to the new async client implementation functions

## 3. Testing and Verification

- [x] 3.1 Update test_mcp.py to include test cases for get_video_analytics and get_channel_video_analytics tools
- [x] 3.2 Verify all tests pass successfully
