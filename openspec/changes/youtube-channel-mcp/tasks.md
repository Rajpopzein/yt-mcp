## 1. Initial Setup and Package Configuration

- [x] 1.1 Initialize Node.js project in the workspace root
- [x] 1.2 Create package.json with dependencies `@modelcontextprotocol/sdk`, `dotenv` and devDependencies `typescript`, `@types/node`
- [x] 1.3 Configure tsconfig.json and package.json build/run scripts
- [x] 1.4 Create .env.example file and add .env to .gitignore

## 2. YouTube API Client Development

- [x] 2.1 Write environment validation to ensure YOUTUBE_API_KEY is present
- [x] 2.2 Write functions to fetch YouTube channel details by channel ID or handle (supporting custom handle normalization)
- [x] 2.3 Write functions to fetch videos of a channel using its uploads playlist ID

## 3. MCP Server Implementation

- [x] 3.1 Initialize the MCP Server using `@modelcontextprotocol/sdk` and configure StdioServerTransport
- [x] 3.2 Define the tool schema and register get_channel_details tool
- [x] 3.3 Define the tool schema and register get_channel_videos tool
- [x] 3.4 Bind tool handler requests to the YouTube API client implementation

## 4. Verification and Packaging

- [x] 4.1 Add instructions on configuring the MCP server in Claude Desktop or other client
- [x] 4.2 Verify the tools manually using a run script or mock test
