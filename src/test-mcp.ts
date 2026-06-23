import { spawn } from 'child_process';
import readline from 'readline';

async function runMcpTest() {
  console.log("Starting MCP Server subprocess...");
  
  // Spawn the compiled MCP server
  const child = spawn('node', ['build/index.js'], {
    env: process.env
  });

  // Log stderr (where the server logs startup/info messages)
  child.stderr.on('data', (data) => {
    console.log(`[Server Stderr]: ${data.toString().trim()}`);
  });

  const rl = readline.createInterface({
    input: child.stdout
  });

  // Helper to send JSON-RPC request and wait for the line-delimited response
  const sendRequest = (req: any): Promise<any> => {
    return new Promise((resolve) => {
      rl.once('line', (line) => {
        resolve(JSON.parse(line));
      });
      child.stdin.write(JSON.stringify(req) + '\n');
    });
  };

  try {
    // 1. Send 'tools/list' request
    console.log("\nSending 'tools/list' request...");
    const listResponse = await sendRequest({
      jsonrpc: "2.0",
      id: 1,
      method: "tools/list",
      params: {}
    });
    console.log("Received 'tools/list' response:", JSON.stringify(listResponse, null, 2));

    // Assert tools are present
    const tools = listResponse.result?.tools || [];
    const hasDetails = tools.some((t: any) => t.name === 'get_channel_details');
    const hasVideos = tools.some((t: any) => t.name === 'get_channel_videos');
    if (hasDetails && hasVideos) {
      console.log("✓ Tools registered successfully in schema.");
    } else {
      throw new Error("Missing expected tools in ListTools response!");
    }

    // 2. Call 'get_channel_details' for '@GoogleDevelopers'
    console.log("\nCalling 'get_channel_details' tool for handle '@GoogleDevelopers'...");
    const callResponse = await sendRequest({
      jsonrpc: "2.0",
      id: 2,
      method: "tools/call",
      params: {
        name: "get_channel_details",
        arguments: {
          handle: "@GoogleDevelopers"
        }
      }
    });
    console.log("Received 'tools/call' response:", JSON.stringify(callResponse, null, 2));
    
    if (callResponse.result?.content?.[0]?.text) {
      const data = JSON.parse(callResponse.result.content[0].text);
      if (data.title === "Google for Developers") {
        console.log("✓ End-to-end MCP communication and YouTube Data query SUCCESSFUL!");
      } else {
        throw new Error(`Unexpected channel title returned: ${data.title}`);
      }
    } else {
      throw new Error("Invalid or empty response format received.");
    }

  } catch (err) {
    console.error("MCP Integration Test Failed:", err);
  } finally {
    child.kill();
    process.exit(0);
  }
}

runMcpTest().catch(console.error);
