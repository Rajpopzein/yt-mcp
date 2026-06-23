import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

/**
 * Validates and retrieves the YouTube API key from the environment.
 * If the key is missing, throws a descriptive error to halt server startup.
 */
export function getApiKey(): string {
  const apiKey = process.env.YOUTUBE_API_KEY;
  if (!apiKey || apiKey.trim() === '' || apiKey === 'your_youtube_api_key_here') {
    throw new Error(
      'YOUTUBE_API_KEY is not defined in the environment. ' +
      'Please create a .env file in the project root with your Google/YouTube API key, ' +
      'e.g. YOUTUBE_API_KEY=AIzaSy...'
    );
  }
  return apiKey;
}
