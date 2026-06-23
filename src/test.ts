import { normalizeHandle, fetchChannelDetails, fetchChannelVideos } from './youtube.js';

async function runTests() {
  console.log("Testing normalizeHandle...");
  const handle1 = normalizeHandle("@GoogleDevelopers");
  const handle2 = normalizeHandle("GoogleDevelopers");
  console.log(`@GoogleDevelopers -> ${handle1} (Expected: GoogleDevelopers)`);
  console.log(`GoogleDevelopers -> ${handle2} (Expected: GoogleDevelopers)`);
  
  if (handle1 !== "GoogleDevelopers" || handle2 !== "GoogleDevelopers") {
    throw new Error("normalizeHandle failed!");
  }
  console.log("✓ normalizeHandle OK");

  // Check if YOUTUBE_API_KEY is configured
  const apiKey = process.env.YOUTUBE_API_KEY;
  if (!apiKey || apiKey === 'your_youtube_api_key_here' || apiKey.trim() === '') {
    console.log("\nSkipping live YouTube API tests because YOUTUBE_API_KEY is not defined in the environment.");
    console.log("To run live tests, create a .env file with YOUTUBE_API_KEY=your_key and run 'npm run build && node build/test.js'");
    return;
  }

  console.log("\nTesting live API fetchChannelDetails by handle 'GoogleDevelopers'...");
  try {
    const details = await fetchChannelDetails({ handle: "GoogleDevelopers" });
    console.log("✓ fetchChannelDetails OK");
    console.log("Channel details:", JSON.stringify(details, null, 2));

    console.log("\nTesting live API fetchChannelVideos...");
    const videos = await fetchChannelVideos(details.uploadsPlaylistId, 3);
    console.log("✓ fetchChannelVideos OK");
    console.log("Recent videos:", JSON.stringify(videos, null, 2));
  } catch (error) {
    console.error("Live API tests failed:", error);
  }
}

runTests().catch(console.error);
