## Why

Users want a way to query YouTube channel statistics and details (such as subscriber counts, view counts, video count, and channel metadata) directly within MCP-compatible clients. This change introduces a YouTube Channel Model Context Protocol (MCP) server that securely integrates with the YouTube Data API v3 using an API key loaded from a `.env` file.

## What Changes

- Add a new MCP server implementation in JavaScript/TypeScript (Node.js) or Python. Let's build a Node.js-based MCP server.
- Integrate with a `.env` file to retrieve the YouTube/Google API Key.
- Implement tools to query YouTube channel details (e.g., `get_channel_details` and `get_channel_videos`).
- Format the output nicely for MCP consumption.

## Capabilities

### New Capabilities
- `youtube-channel-info`: Retrieve YouTube channel metadata, statistics, and list of videos via MCP tools.

### Modified Capabilities
