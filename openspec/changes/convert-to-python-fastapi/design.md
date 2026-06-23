## Context

We are migrating the YouTube Channel MCP server from Node.js (Stdio transport) to Python FastAPI (SSE transport). This makes the server deployable to serverless hosting platforms like Vercel and auto-generates interactive Swagger API documentation.

## Goals / Non-Goals

**Goals:**
- Rewrite the YouTube Data API client in Python using `httpx` (async).
- Implement the MCP server using Python's `FastMCP` high-level SDK.
- Integrate the MCP server into a FastAPI web application using Server-Sent Events (SSE).
- Serve auto-generated Swagger/OpenAPI docs at `/docs` for the web endpoints.
- Manage settings and API keys via `python-dotenv`.

**Non-Goals:**
- Keeping TypeScript/Node.js files in the workspace (we will clean them up after implementation).
- Custom OAuth 2.0 flow.

## Decisions

- **Runtime & Web Framework**: Python 3.10+ with FastAPI and Uvicorn.
- **MCP Python SDK**: `FastMCP` (from the official `mcp` SDK), which abstracts away the low-level JSON-RPC protocol handling.
- **HTTP Client**: Async `httpx` client to make non-blocking HTTP requests to the YouTube Data API endpoints.
- **SSE Mounting**: Mount the FastMCP SSE server directly onto the FastAPI instance via `app.mount("/", mcp.sse_app())`. This handles:
  - `GET /sse`: Establishes the event stream.
  - `POST /messages`: Handshakes JSON-RPC requests.
- **Dependency Management**: Use a standard `requirements.txt` listing `fastapi`, `uvicorn`, `fastmcp`, `python-dotenv`, and `httpx`.

## Risks / Trade-offs

- **Serverless Execution Limits**: If hosted on Vercel Serverless Functions, SSE connections might be subject to execution timeouts (e.g., 10 seconds for hobby tier). However, YouTube API queries take less than 1 second, so this is perfectly safe for executing individual tool calls.
