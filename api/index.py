import json
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from api.youtube import fetch_channel_details, fetch_channel_videos

# Initialize FastMCP server
mcp = FastMCP("youtube-channel-mcp")

# Register MCP tools
@mcp.tool(
    name="get_channel_details",
    description="Retrieve YouTube channel details, statistics (subscribers, views, videos), and uploads playlist ID by channel ID or handle."
)
async def get_channel_details(
    channel_id: Optional[str] = None,
    handle: Optional[str] = None
) -> str:
    """
    Retrieve YouTube channel details and statistics.
    :param channel_id: The unique YouTube channel ID (e.g. UC_x5XG1OV2P6uZZ5FSM9Ttw)
    :param handle: The channel custom handle (e.g. @GoogleDevelopers or GoogleDevelopers)
    """
    if not channel_id and not handle:
        return "Error: You must provide either 'channel_id' or 'handle'."
    
    try:
        details = await fetch_channel_details(channel_id=channel_id, handle=handle)
        return json.dumps(details, indent=2)
    except Exception as e:
        return f"Error fetching channel details: {str(e)}"

@mcp.tool(
    name="get_channel_videos",
    description="Retrieve uploaded videos for a channel by channel ID or handle."
)
async def get_channel_videos(
    channel_id: Optional[str] = None,
    handle: Optional[str] = None,
    limit: int = 10
) -> str:
    """
    Retrieve recent video uploads for a channel.
    :param channel_id: The unique YouTube channel ID
    :param handle: The channel custom handle
    :param limit: Maximum number of videos to return (default 10, max 50)
    """
    if not channel_id and not handle:
        return "Error: You must provide either 'channel_id' or 'handle'."
    
    try:
        # Resolve uploads playlist ID first via details
        details = await fetch_channel_details(channel_id=channel_id, handle=handle)
        videos = await fetch_channel_videos(details["uploadsPlaylistId"], limit=limit)
        
        result = {
            "channelTitle": details["title"],
            "channelId": details["id"],
            "videos": videos
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error fetching channel videos: {str(e)}"

# Create FastAPI app
app = FastAPI(
    title="YouTube Channel MCP API",
    description="FastAPI application hosting a YouTube Channel Model Context Protocol (MCP) server over SSE.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware to allow connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "YouTube Channel MCP Server",
        "documentation": "/docs",
        "mcp_sse_endpoint": "/sse",
        "mcp_messages_endpoint": "/messages"
    }

# Mount the MCP server's SSE application at the root
app.mount("/", mcp.sse_app())
