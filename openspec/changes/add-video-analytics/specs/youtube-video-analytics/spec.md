## ADDED Requirements

### Requirement: Query Video Analytics by ID
The system SHALL provide an MCP tool named `get_video_analytics` to query metrics (views, likes, comments) and metadata (title, duration, description, resolution) for one or more video IDs.

#### Scenario: Retrieve single video analytics
- **WHEN** `get_video_analytics` is called with a single valid `video_id` (e.g., `bfvS1UeAkN0`)
- **THEN** the system returns a JSON representation containing the video's details and statistics (views, likes, comments, duration, dimension, definition)

#### Scenario: Retrieve multiple videos analytics
- **WHEN** `get_video_analytics` is called with a list of comma-separated valid `video_ids` (e.g., `bfvS1UeAkN0,qnl8-PBJNu4`)
- **THEN** the system queries the API in a single batch request and returns a list containing analytics for all specified videos

### Requirement: Query Channel Video Analytics
The system SHALL provide an MCP tool named `get_channel_video_analytics` to retrieve recently uploaded videos for a channel along with their full performance analytics.

#### Scenario: Retrieve recent videos with detailed metrics
- **WHEN** `get_channel_video_analytics` is called with a valid `channel_id` or `handle` and a `limit` of 5
- **THEN** the system resolves the uploads playlist, retrieves the recent 5 videos, queries detailed metrics for all 5 videos in a batch, and returns the list of videos populated with views, likes, comments, duration, and resolution
