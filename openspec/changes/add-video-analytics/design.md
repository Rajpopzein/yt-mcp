## Context

The Python MCP server retrieves basic channel statistics and public video analytics (views, likes, comments, duration, definition) from the YouTube Data API. To expose private, deep analytics metrics (such as impressions, CTR, watch time, and subscriber gains/losses) for the authenticated channel, we will integrate the YouTube Analytics API using an OAuth2 token refresh flow.

## Goals / Non-Goals

**Goals:**
- Implement an OAuth2 access token refresh client helper in `api/youtube.py` that refreshes tokens dynamically using client credentials and a refresh token from the environment.
- Cache the access token in memory to avoid token refresh requests on every tool call.
- Query private video reports from the YouTube Analytics API endpoint: `GET https://youtubeanalytics.googleapis.com/v2/reports`.
- Fetch `views`, `estimatedMinutesWatched`, `averageViewDuration`, `averageViewPercentage`, `subscribersGained`, `subscribersLost`, `likes`, `comments`, `shares`, `video_thumbnail_impressions`, and `video_thumbnail_impressions_click_rate` metrics.
- Merge the private analytics fields under an `analytics` key in `get_video_analytics` and `get_channel_video_analytics` responses.
- Fall back gracefully to public-only metrics if OAuth2 credentials are not set up or invalid.

**Non-Goals:**
- Direct user interactive OAuth2 redirects. The server is designed to run non-interactively using static client credentials and a refresh token.

## Decisions

- **Token Refresh Endpoint**: `POST https://oauth2.googleapis.com/token` with urlencoded form parameters (`client_id`, `client_secret`, `refresh_token`, `grant_type=refresh_token`).
- **Reports Query Endpoint**: `GET https://youtubeanalytics.googleapis.com/v2/reports` with parameters:
  - `ids=channel==MINE`
  - `startDate=2005-01-01`
  - `endDate=<current_date>`
  - `metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares,video_thumbnail_impressions,video_thumbnail_impressions_click_rate`
  - `dimensions=video`
  - `filters=video==<video_id_1>,<video_id_2>,...`
- **Graceful Error Recovery**: If query fails on `video_thumbnail_impressions` or other metrics, query again using a fallback list of core metrics to ensure high resilience.
- **Access Token Caching**: Maintain `_token_cache` in-memory. Refresh only when within 60 seconds of expiration.

## Risks / Trade-offs

- **Security of Refresh Token**: The refresh token has full access to YouTube Analytics. It must be kept secure in environment variables and never committed to source control.
- **Data Latency**: YouTube Analytics API data is not in real-time and has up to 1-2 days of latency. This is a characteristic of the YouTube Analytics platform itself.

