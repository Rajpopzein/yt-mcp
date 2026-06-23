## Context

The current Python MCP server retrieves basic channel statistics and lists uploads, but does not provide rich performance metrics (views, likes, comments) or content metadata (duration, resolution, definition) for individual videos. We will implement these capabilities by integrating the YouTube Data API `/videos` endpoint.

## Goals / Non-Goals

**Goals:**
- Implement an async function in `api/youtube.py` to fetch video details from `/youtube/v3/videos`.
- Expose the `get_video_analytics` tool to fetch statistics for a list of video IDs.
- Expose the `get_channel_video_analytics` tool to fetch recent uploads for a channel with their metrics resolved and populated in a single call.
- Support batching up to 50 video IDs in a single request to conserve API quotas and reduce network latency.

**Non-Goals:**
- Integrating the YouTube Analytics API (which requires OAuth 2.0 user login). All data will be queried using the public YouTube Data API v3 and the configured API Key.

## Decisions

- **YouTube Videos Endpoint**: `/youtube/v3/videos?part=snippet,statistics,contentDetails&id={ids}&key={apiKey}`.
- **Batch Processing**: The `id` parameter takes a comma-separated list of IDs. We will split input strings, clean up whitespaces, chunk into lists of max 50 items (YouTube API limit), and query them in batches.
- **Data Enrichment**: When querying channel video analytics, the server will first fetch the list of uploads using `fetch_channel_videos` (which returns only basic data like titles and IDs), then extract the video IDs, and call the batch video details endpoint to return fully populated analytics objects for the channel.
- **Metadata Returned**:
  - Statistics: `viewCount`, `likeCount`, `commentCount`.
  - Content Details: `duration` (ISO 8601 duration), `dimension`, `definition` (hd/sd), `projection`.

## Risks / Trade-offs

- **YouTube API Quotas**: Resolving a channel's videos details takes 2 API requests (1 for playlist items and 1 for batch video details), costing only 2 quota units. This remains highly performant and secure against quota exhaustion.
