## 1. Project Configuration and Setup

- [x] 1.1 Create requirements.txt with dependencies fastapi, fastmcp, uvicorn, python-dotenv, httpx
- [x] 1.2 Remove legacy Node.js configuration files (package.json, tsconfig.json, build/, src/, node_modules/)

## 2. Python YouTube Client Implementation

- [x] 2.1 Write config.py to load and validate YOUTUBE_API_KEY from environment
- [x] 2.2 Write youtube.py using httpx to fetch channel details by ID or handle (with handle normalization)
- [x] 2.3 Write youtube.py uploads playlist video fetch function using uploads playlist ID

## 3. FastAPI and MCP SSE Server

- [x] 3.1 Initialize the FastMCP instance and define get_channel_details tool
- [x] 3.2 Define get_channel_videos tool in the FastMCP instance
- [x] 3.3 Create FastAPI app, mount the FastMCP SSE application at the root, and configure Swagger docs
- [x] 3.4 Bind tool methods to the async YouTube API client implementation

## 4. Documentation and Verification

- [x] 4.1 Create vercel.json and update README.md with Python FastAPI setup and Swagger docs details
- [x] 4.2 Write a Python integration test script test_mcp.py to simulate SSE MCP JSON-RPC connection
- [x] 4.3 Verify all tests pass and server successfully serves the Swagger docs at /docs
