# YouTube Channel MCP Server (Python FastAPI)

A Model Context Protocol (MCP) server that retrieves YouTube Channel statistics, metadata, and uploaded videos using the YouTube Data API v3. 

This version is implemented in **Python** using **FastAPI** and the **FastMCP SDK**. It runs as an HTTP service over **Server-Sent Events (SSE)**, making it ready for local development and cloud hosting on platforms like **Vercel**.

## Features

- **Server-Sent Events (SSE) Transport**: Host your MCP server as a remote service.
- **Auto-generated Docs**: Swagger/OpenAPI interactive documentation automatically available at `/docs`.
- **Flexible Queries**: Search channel statistics and uploads using either a channel ID or handle (automatically handles `@` prefix normalization).
- **Vercel Ready**: Contains a pre-configured `vercel.json` routing configuration.

---

## Local Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Add Environment Variables**:
   Create a `.env` file in the project root:
   ```env
   YOUTUBE_API_KEY=your_google_youtube_api_key_here
   ```

3. **Run the Server**:
   Start the FastAPI development server using Uvicorn:
   ```bash
   uvicorn api.index:app --reload
   ```
   The server will start at `http://127.0.0.1:8000`.

---

## Interactive API Documentation

Once the server is running, you can access the interactive Swagger UI in your browser:
- **Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

You can test endpoints and check request/response schemas directly from the Swagger UI.

---

## Connecting to Claude Desktop (SSE Mode)

To connect Claude Desktop to your locally running FastAPI server, edit your configuration file:

- **Windows Path**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS Path**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the server to `mcpServers` using the `url` property:

```json
{
  "mcpServers": {
    "youtube-channel-info-sse": {
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

*Ensure your FastAPI server is running (`uvicorn api.index:app`) before restarting Claude Desktop.*

---

## Deploying to Vercel

Because this server uses the SSE transport over standard HTTP endpoints, you can deploy it directly to Vercel:

1. Push your repository to GitHub.
2. Go to [Vercel](https://vercel.com/) and import your project.
3. In **Settings -> Environment Variables**, add your:
   - `YOUTUBE_API_KEY` = `<your_api_key>`
4. Deploy! 

Vercel will build the serverless functions. Your live remote MCP URL will be:
`https://your-project.vercel.app/sse`
You can then share this URL or use it in any remote-compatible MCP client configuration!

---

## Available Tools

### 1. `get_channel_details`
Retrieves YouTube channel metadata and statistics.
- **Arguments**:
  - `channel_id` (string, optional): Unique ID of the channel (e.g. `UC_x5XG1OV2P6uZZ5FSM9Ttw`).
  - `handle` (string, optional): Custom handle of the channel (e.g. `@GoogleDevelopers` or `GoogleDevelopers`).

### 2. `get_channel_videos`
Retrieves recently uploaded videos for a channel.
- **Arguments**:
  - `channel_id` (string, optional)
  - `handle` (string, optional)
  - `limit` (number, optional, default: 10, max: 50): Number of videos to retrieve.
