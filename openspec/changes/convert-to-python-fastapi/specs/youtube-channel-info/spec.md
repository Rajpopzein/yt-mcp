## ADDED Requirements

### Requirement: FastAPI SSE Transport Exposing Tools
The system SHALL expose the YouTube MCP server tools over an HTTP Server-Sent Events (SSE) transport using Python FastAPI.

#### Scenario: Initiate SSE connection
- **WHEN** a client makes a GET request to `/sse`
- **THEN** the system responds with an SSE event stream (content-type: `text/event-stream`) and initializes an MCP session

#### Scenario: Client sends message
- **WHEN** a client sends a POST request with a JSON-RPC message to `/messages`
- **THEN** the system processes the message in the current session and returns a 200/202 status code

### Requirement: Swagger API Documentation
The system SHALL auto-generate interactive API documentation (Swagger UI) accessible via the browser.

#### Scenario: Access documentation URL
- **WHEN** the browser navigates to `/docs`
- **THEN** the system renders the interactive OpenAPI/Swagger UI page listing `/sse` and `/messages` endpoints

## MODIFIED Requirements

### Requirement: YouTube API Authentication
The system SHALL load the YouTube/Google API key from the environment variables (e.g., via `.env` file) and authenticate all API requests.

#### Scenario: Load API key from environment
- **WHEN** the server is started with a valid `.env` file containing `YOUTUBE_API_KEY`
- **THEN** the server starts successfully and uses the API key for external calls

#### Scenario: Missing API key
- **WHEN** the server is started without `YOUTUBE_API_KEY` in the environment
- **THEN** the server fails to start or throws a clear error indicating the API key is missing

### Requirement: Get Channel Details
The system SHALL provide an MCP tool named `get_channel_details` to retrieve YouTube channel metadata (title, description, custom URL, creation date) and statistics (subscriber count, video count, view count) by channel ID or handle.

#### Scenario: Retrieve channel details by ID
- **WHEN** `get_channel_details` is called with a valid `channelId` (e.g., `UC_x5XG1OV2P6uZZ5FSM9Ttw`)
- **THEN** the system returns a JSON representation of the channel's details and statistics

#### Scenario: Retrieve channel details by handle
- **WHEN** `get_channel_details` is called with a valid `handle` (e.g., `@GoogleDevelopers` or `GoogleDevelopers`)
- **THEN** the system normalizes the handle (removes `@` if present) and retrieves and returns the channel details

### Requirement: Get Channel Videos
The system SHALL provide an MCP tool named `get_channel_videos` that retrieves the list of videos uploaded by a YouTube channel (using its upload playlist ID) with options for pagination/limit.

#### Scenario: Retrieve recent videos
- **WHEN** `get_channel_videos` is called with a valid `channelId` and a `limit` of 5
- **THEN** the system resolves the uploads playlist ID for the channel, fetches the playlist items, and returns the 5 most recent videos including titles, descriptions, video IDs, and publish dates
