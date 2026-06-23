## Why

Users need a way to retrieve detailed performance metrics (such as view counts, like counts, and comment counts) and metadata (such as video duration and resolution) for specific YouTube videos. Adding video-level analytics enables users to analyze content performance directly via MCP.

## What Changes

- Expose a new tool `get_video_analytics` to query metrics and metadata for specific YouTube video IDs.
- Expose a new tool `get_channel_video_analytics` to fetch recent uploads from a channel and return them enriched with detailed analytics (likes, views, comments, duration).
- Implement batch querying of the YouTube Data API `/videos` endpoint (up to 50 videos at once) for high performance.

## Capabilities

### New Capabilities
- `youtube-video-analytics`: Retrieve metrics (views, likes, comments) and metadata (duration, resolution, tags) for individual videos or a list of videos.

### Modified Capabilities
