
import json
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from api.youtube import fetch_channel_details, fetch_channel_videos, fetch_video_details, fetch_channel_video_analytics

# Initialize FastMCP server with DNS rebinding protection disabled
# This prevents "invalid header" / "invalid origin" errors when accessed by web/desktop clients or hosted on Vercel.
mcp = FastMCP(
    "youtube-channel-mcp",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False)
)

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

@mcp.tool(
    name="get_video_analytics",
    description="Retrieve performance metrics (views, likes, comments) and metadata (duration, definition, tags) for one or more YouTube video IDs (comma-separated)."
)
async def get_video_analytics(video_ids: str) -> str:
    """
    Retrieve YouTube video performance statistics.
    :param video_ids: A comma-separated list of video IDs (e.g. bfvS1UeAkN0, qnl8-PBJNu4)
    """
    if not video_ids or video_ids.strip() == "":
        return "Error: You must provide a comma-separated list of video IDs."
    
    ids_list = [vid.strip() for vid in video_ids.split(",") if vid.strip()]
    if not ids_list:
        return "Error: No valid video IDs provided."
        
    try:
        videos = await fetch_video_details(ids_list)
        return json.dumps(videos, indent=2)
    except Exception as e:
        return f"Error fetching video analytics: {str(e)}"

@mcp.tool(
    name="get_channel_video_analytics",
    description="Retrieve recently uploaded videos for a channel fully populated with detailed performance statistics (views, likes, comments, duration, resolution)."
)
async def get_channel_video_analytics(
    channel_id: Optional[str] = None,
    handle: Optional[str] = None,
    limit: int = 10
) -> str:
    """
    Retrieve performance analytics for the recently uploaded videos of a channel.
    :param channel_id: The unique YouTube channel ID
    :param handle: The channel custom handle
    :param limit: Maximum number of videos to return (default 10, max 50)
    """
    if not channel_id and not handle:
        return "Error: You must provide either 'channel_id' or 'handle'."
        
    try:
        analytics = await fetch_channel_video_analytics(channel_id=channel_id, handle=handle, limit=limit)
        return json.dumps(analytics, indent=2)
    except Exception as e:
        return f"Error fetching channel video analytics: {str(e)}"


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
