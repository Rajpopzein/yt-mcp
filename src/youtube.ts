import { getApiKey } from './config.js';

export interface ChannelDetails {
  id: string;
  title: string;
  description: string;
  customUrl?: string;
  publishedAt: string;
  statistics: {
    viewCount: string;
    subscriberCount: string;
    hiddenSubscriberCount: boolean;
    videoCount: string;
  };
  uploadsPlaylistId: string;
}

export interface VideoDetails {
  videoId: string;
  title: string;
  description: string;
  publishedAt: string;
  url: string;
}

/**
 * Normalizes user handle input by removing leading '@' if present.
 */
export function normalizeHandle(handle: string): string {
  let h = handle.trim();
  if (h.startsWith('@')) {
    h = h.substring(1);
  }
  return h;
}

/**
 * Fetches YouTube channel statistics and metadata by channel ID or handle.
 */
export async function fetchChannelDetails(identifier: { id?: string; handle?: string }): Promise<ChannelDetails> {
  const apiKey = getApiKey();
  let url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails';
  
  if (identifier.id) {
    url += `&id=${encodeURIComponent(identifier.id.trim())}`;
  } else if (identifier.handle) {
    const handle = normalizeHandle(identifier.handle);
    url += `&forHandle=${encodeURIComponent(handle)}`;
  } else {
    throw new Error('Must provide either channel ID or custom handle.');
  }
  
  url += `&key=${apiKey}`;

  const response = await fetch(url);
  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`YouTube API error (${response.status}): ${errText}`);
  }

  const data = (await response.json()) as any;
  if (!data.items || data.items.length === 0) {
    throw new Error(`No channel found for identifier: ${identifier.id || identifier.handle}`);
  }

  const item = data.items[0];
  return {
    id: item.id,
    title: item.snippet.title,
    description: item.snippet.description,
    customUrl: item.snippet.customUrl,
    publishedAt: item.snippet.publishedAt,
    statistics: {
      viewCount: item.statistics.viewCount,
      subscriberCount: item.statistics.subscriberCount,
      hiddenSubscriberCount: item.statistics.hiddenSubscriberCount,
      videoCount: item.statistics.videoCount,
    },
    uploadsPlaylistId: item.contentDetails.relatedPlaylists.uploads,
  };
}

/**
 * Fetches recent video uploads for a channel using its uploads playlist ID.
 */
export async function fetchChannelVideos(uploadsPlaylistId: string, limit: number = 10): Promise<VideoDetails[]> {
  const apiKey = getApiKey();
  const maxResults = Math.min(Math.max(limit, 1), 50); // Clamp limit between 1 and 50
  
  const url = `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=${encodeURIComponent(
    uploadsPlaylistId
  )}&maxResults=${maxResults}&key=${apiKey}`;

  const response = await fetch(url);
  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`YouTube API error (${response.status}): ${errText}`);
  }

  const data = (await response.json()) as any;
  if (!data.items) {
    return [];
  }

  return data.items.map((item: any) => ({
    videoId: item.snippet.resourceId.videoId,
    title: item.snippet.title,
    description: item.snippet.description,
    publishedAt: item.snippet.publishedAt,
    url: `https://www.youtube.com/watch?v=${item.snippet.resourceId.videoId}`,
  }));
}
