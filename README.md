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

### 3. `get_video_analytics`
Retrieves public statistics (views, likes, comments) and metadata (duration, definition). When OAuth2 is configured, it also fetches private Analytics API metrics (impressions, CTR, watch time, retention/average percentage, subscriber gains/losses, shares).
- **Arguments**:
  - `video_ids` (string, required): Comma-separated list of video IDs (e.g. `bfvS1UeAkN0,qnl8-PBJNu4`).

### 4. `get_channel_video_analytics`
Retrieves recent uploads for a channel fully enriched with public statistics and private Analytics API metrics (if OAuth2 is configured).
- **Arguments**:
  - `channel_id` (string, optional)
  - `handle` (string, optional)
  - `limit` (number, optional, default: 10, max: 50)

---

## Private YouTube Analytics Setup (OAuth2)

To retrieve private video-level performance metrics (such as CTR, impressions, average watch duration, and subscriber changes), you must obtain Google OAuth2 Client credentials and a refresh token.

### 1. Google Cloud Console Setup
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Enable both the **YouTube Analytics API** and the **YouTube Data API v3**.
4. Configure the **OAuth Consent Screen**:
   - Choose **External** user type.
   - Enter standard details (AppName, Support Email).
   - Add your own email as a **Test User** (required while in testing status).
5. Create Credentials:
   - Go to **Credentials** -> **Create Credentials** -> **OAuth Client ID**.
   - Select **Web application** as application type.
   - Add `http://localhost:8080/` under **Authorized redirect URIs**.
   - Copy the generated **Client ID** and **Client Secret**.

### 2. Generate the Refresh Token
You can easily generate your refresh token using the helper script included in the repository:
1. Run the helper script:
   ```bash
   python get_refresh_token.py
   ```
2. Enter your **Client ID** and **Client Secret** when prompted.
3. The script will automatically open your web browser to sign in to your Google Account.
4. Sign in with the account owning the YouTube channel and grant the permissions.
5. Return to your terminal to copy the generated **Refresh Token**.

### 3. Environment Variables
Add the generated credentials to your `.env` (or Vercel Environment Variables):
```env
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret
YOUTUBE_REFRESH_TOKEN=your_refresh_token
```

