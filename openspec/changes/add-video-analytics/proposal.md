## Why

Users need access to private, deep video performance metrics (such as watch time, average view duration, average view percentage/retention, and subscriber changes) for their own YouTube channel. These metrics are not available in the public YouTube Data API and require integration with the secure YouTube Analytics API via OAuth2.

## What Changes

- Support secure OAuth2 token refresh in Python using a client ID, client secret, and refresh token loaded from the `.env` file.
- Implement integration with the YouTube Analytics API (`youtubeanalytics.googleapis.com/v2/reports`) to retrieve private video metrics:
  - `views`: Total views.
  - `estimatedMinutesWatched`: Total watch time in minutes.
  - `averageViewDuration`: Average watch duration in seconds.
  - `averageViewPercentage`: Retention rate percentage.
  - `subscribersGained` / `subscribersLost`: Subscriber impact.
  - `likes` / `comments` / `shares`: Deeper engagement metrics.
- Update `get_video_analytics` to return both public Data API stats and private Analytics API stats when OAuth2 credentials are provided.
- Provide a detailed guide in `README.md` on how to obtain Google OAuth2 credentials and a refresh token.

## Capabilities

### New Capabilities
- `youtube-video-analytics`: Retrieve public metadata/statistics, plus private YouTube Analytics API metrics (watch time, retention, subscriber impact) via OAuth2.

### Modified Capabilities
