# YouTube Channel MCP Server

A Model Context Protocol (MCP) server that retrieves YouTube Channel information, statistics, and videos using the official YouTube Data API v3. Communication is performed over standard input/output (stdio) transport.

## Features

- **Query by Channel ID or Custom Handle**: Retrieve channel title, description, subscriber count, total views, video count, etc.
- **Normalize Handles**: Strips leading `@` from custom handles automatically.
- **List Recent Videos**: Dynamically fetches recently uploaded videos from a channel using its upload playlist (saves API quota).
- **Environment-based configuration**: Loads the API key securely from a `.env` file or environment variables.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env` file in the project root:
   ```env
   YOUTUBE_API_KEY=your_google_youtube_api_key_here
   ```

3. Build the TypeScript code:
   ```bash
   npm run build
   ```

## Configuration in Claude Desktop

Add this configuration to your Claude Desktop config file:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "youtube-channel-info": {
      "command": "node",
      "args": ["D:/mcpyt/build/index.js"],
      "env": {
        "YOUTUBE_API_KEY": "your_google_youtube_api_key_here"
      }
    }
  }
}
```

*Note: Replace `D:/mcpyt` with the actual absolute path to your project folder.*

## Available Tools

### 1. `get_channel_details`
Retrieves YouTube channel metadata and statistics.
- **Arguments**:
  - `channelId` (string, optional): Unique ID of the channel (e.g. `UC_x5XG1OV2P6uZZ5FSM9Ttw`).
  - `handle` (string, optional): Custom handle of the channel (e.g. `@GoogleDevelopers` or `GoogleDevelopers`).

### 2. `get_channel_videos`
Retrieves recently uploaded videos for a channel.
- **Arguments**:
  - `channelId` (string, optional)
  - `handle` (string, optional)
  - `limit` (number, optional, default: 10, max: 50): Number of videos to retrieve.
