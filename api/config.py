import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

def get_api_key() -> str:
    """
    Validates and retrieves the YouTube API key from the environment.
    If the key is missing or is set to a placeholder, raises a ValueError.
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "your_youtube_api_key_here":
        raise ValueError(
            "YOUTUBE_API_KEY is not defined in the environment. "
            "Please create a .env file in the project root containing your API key: "
            "YOUTUBE_API_KEY=your_actual_key"
        )
    return api_key.strip()
