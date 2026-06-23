## Context

This project implements a Model Context Protocol (MCP) server that connects to the YouTube Data API v3 to retrieve channel details and list channel videos. It is built as a Node.js project from scratch and uses standard MCP stdio transport to communicate with the client.

## Goals / Non-Goals

**Goals:**
- Initialize a Node.js project with TypeScript.
- Build an MCP server using `@modelcontextprotocol/sdk`.
- Implement a `.env` file loader using the `dotenv` package.
- Expose MCP tools:
  - `get_channel_details`: Retrieves statistics (subscribers, views, video counts) and basic metadata (title, description, custom URL) by channel ID or handle.
  - `get_channel_videos`: Retrieves a list of the channel's uploaded videos by querying its upload playlist.
- Support handle normalization (automatically stripping the leading `@` symbol if provided).

**Non-Goals:**
- OAuth2 authentication or write-level APIs (e.g., uploading videos, subscribing, commenting).
- Bulky SDK dependencies (using direct REST calls to YouTube Data API instead of the large `googleapis` library).

## Decisions

- **Runtime & SDK**: Node.js with TypeScript and the official `@modelcontextprotocol/sdk` (Stdio transport).
- **HTTP Client**: Built-in `fetch` (Node.js 18+) or `axios` for simplicity and lightweight execution, bypassing the `googleapis` library.
- **YouTube Channels Endpoint**:
  - By Channel ID: `/youtube/v3/channels?part=snippet,statistics,contentDetails&id={id}`
  - By Handle: `/youtube/v3/channels?part=snippet,statistics,contentDetails&forHandle={handle}`
- **Retrieve Videos via Uploads Playlist**: Instead of using the expensive `/youtube/v3/search` endpoint (which costs 100 quota units per call), we will extract the `uploads` playlist ID from the channel's `contentDetails.relatedPlaylists.uploads` object, then query `/youtube/v3/playlistItems?part=snippet&playlistId={uploadsPlaylistId}` (which costs only 1 quota unit).

## Risks / Trade-offs

- **YouTube API Quotas**: YouTube Data API v3 has a daily limit of 10,000 units. Using `/channels` and `/playlistItems` costs only 1 unit per request, ensuring the server does not exhaust quotas under normal development/testing usage.
- **API Key Security**: The API key must never be hardcoded or checked into source control. We will load it via `dotenv` from a local `.env` file, and include `.env` in `.gitignore`.
