import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ErrorCode,
  McpError,
} from "@modelcontextprotocol/sdk/types.js";
import { fetchChannelDetails, fetchChannelVideos } from "./youtube.js";

// Initialize the MCP server
const server = new Server(
  {
    name: "youtube-channel-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Register tools and define schemas
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_channel_details",
        description: "Retrieve YouTube channel details, statistics (subscribers, views, videos), and uploads playlist ID by channel ID or handle",
        inputSchema: {
          type: "object",
          properties: {
            channelId: {
              type: "string",
              description: "The unique YouTube channel ID (e.g., UC_x5XG1OV2P6uZZ5FSM9Ttw)",
            },
            handle: {
              type: "string",
              description: "The channel handle, with or without '@' prefix (e.g., @GoogleDevelopers or GoogleDevelopers)",
            },
          },
        },
      },
      {
        name: "get_channel_videos",
        description: "Retrieve uploaded videos for a channel by channel ID or handle",
        inputSchema: {
          type: "object",
          properties: {
            channelId: {
              type: "string",
              description: "The unique YouTube channel ID",
            },
            handle: {
              type: "string",
              description: "The channel handle, with or without '@' prefix",
            },
            limit: {
              type: "number",
              description: "Maximum number of videos to return (default 10, max 50)",
              default: 10,
            },
          },
        },
      },
    ],
  };
});

// Handle tool execution requests
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "get_channel_details") {
      const channelId = args?.channelId as string | undefined;
      const handle = args?.handle as string | undefined;

      if (!channelId && !handle) {
        throw new McpError(
          ErrorCode.InvalidParams,
          "You must provide either 'channelId' or 'handle'."
        );
      }

      const details = await fetchChannelDetails({ id: channelId, handle });
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(details, null, 2),
          },
        ],
      };
    }

    if (name === "get_channel_videos") {
      const channelId = args?.channelId as string | undefined;
      const handle = args?.handle as string | undefined;
      const limit = typeof args?.limit === "number" ? args.limit : 10;

      if (!channelId && !handle) {
        throw new McpError(
          ErrorCode.InvalidParams,
          "You must provide either 'channelId' or 'handle'."
        );
      }

      // Fetch channel details first to resolve the uploads playlist ID
      const details = await fetchChannelDetails({ id: channelId, handle });
      const videos = await fetchChannelVideos(details.uploadsPlaylistId, limit);

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                channelTitle: details.title,
                channelId: details.id,
                videos,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    throw new McpError(
      ErrorCode.MethodNotFound,
      `Unknown tool: ${name}`
    );
  } catch (error: any) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      content: [
        {
          type: "text",
          text: `Error executing tool: ${message}`,
        },
      ],
      isError: true,
    };
  }
});

// Run server using stdio transport
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("YouTube Channel MCP Server running on stdio transport");
}

main().catch((error) => {
  console.error("Error starting YouTube Channel MCP Server:", error);
  process.exit(1);
});
