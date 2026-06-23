## Why

Converting the existing Node.js Stdio server to a Python FastAPI server enables hosting the MCP server as a web service over Server-Sent Events (SSE). This allows it to be hosted on serverless platforms like Vercel and auto-generates interactive API documentation (Swagger UI) at `/docs`.

## What Changes

- **BREAKING**: Migrate from Node.js (TypeScript) to Python 3.10+.
- Reimplement the YouTube MCP server using the Python MCP SDK (`mcp` package).
- Integrate FastAPI to serve the MCP protocol over SSE transport.
- Expose endpoints:
  - `/sse`: Endpoint to initiate Server-Sent Events MCP connection.
  - `/messages`: Endpoint to receive MCP client JSON-RPC messages.
  - `/docs`: Swagger UI containing auto-generated documentation for the endpoints.
- Manage dependencies using a `requirements.txt` file.

## Capabilities

### New Capabilities

### Modified Capabilities
- `youtube-channel-info`: Convert connection transport from stdio to Server-Sent Events (SSE) using HTTP endpoints.

## Impact

- Replaces the Node.js project layout (`package.json`, `tsconfig.json`, `src/` directory, `build/` directory) with a Python-based project structure.
- Replaces Node dependencies with Python libraries (`fastapi`, `uvicorn`, `mcp`, `python-dotenv`, `httpx`).
