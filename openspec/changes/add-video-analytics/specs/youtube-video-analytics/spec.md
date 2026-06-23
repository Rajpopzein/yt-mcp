## ADDED Requirements

### Requirement: Query Video Analytics by ID
The system SHALL provide an MCP tool named `get_video_analytics` to query metrics (views, likes, comments) and metadata (title, duration, description, resolution) for one or more video IDs. When OAuth2 credentials are configured, the system SHALL retrieve private Analytics API metrics (impressions, CTR, watch time, retention/average percentage, subscriber gains/losses, shares).

#### Scenario: Retrieve single video analytics with OAuth2 configured
- **WHEN** `get_video_analytics` is called with a single valid `video_id` (e.g., `bfvS1UeAkN0`) and OAuth2 credentials are configured in `.env`
- **THEN** the system returns a JSON representation containing the video's public details, statistics, and an `analytics` object containing private metrics (views, estimatedMinutesWatched, averageViewDuration, averageViewPercentage, subscribersGained, subscribersLost, likes, comments, shares, video_thumbnail_impressions, video_thumbnail_impressions_click_rate)

#### Scenario: Retrieve single video analytics with OAuth2 missing
- **WHEN** `get_video_analytics` is called with a single valid `video_id` and OAuth2 credentials are not configured
- **THEN** the system returns a JSON representation containing the public details and statistics, omitting the private `analytics` object without raising an error

#### Scenario: Retrieve multiple videos analytics
- **WHEN** `get_video_analytics` is called with a list of comma-separated valid `video_ids` (e.g., `bfvS1UeAkN0,qnl8-PBJNu4`)
- **THEN** the system queries the APIs and returns a list containing analytics for all specified videos

### Requirement: Query Channel Video Analytics
The system SHALL provide an MCP tool named `get_channel_video_analytics` to retrieve recently uploaded videos for a channel along with their full performance analytics (including private analytics if OAuth2 is configured).

#### Scenario: Retrieve recent videos with detailed metrics
- **WHEN** `get_channel_video_analytics` is called with a valid `channel_id` or `handle` and a `limit` of 5
- **THEN** the system resolves the uploads playlist, retrieves the recent 5 videos, queries metrics for all 5 videos in a batch, and returns the list of videos populated with their public and private performance details

