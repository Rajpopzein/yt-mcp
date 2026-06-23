import os
import sys
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import httpx

# Local port to run redirect server
PORT = 8080
REDIRECT_URI = f"http://localhost:{PORT}/"

# Global variable to capture the auth code
auth_code = None

class OAuthRedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        
        if "code" in params:
            auth_code = params["code"][0]
            self.wfile.write(b"<h1>Authorization Successful!</h1><p>You can close this tab and return to the terminal.</p>")
        else:
            self.wfile.write(b"<h1>Authorization Failed!</h1><p>No code parameter found in callback URL.</p>")

def get_tokens(client_id, client_secret, code):
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = httpx.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to exchange token ({response.status_code}): {response.text}")

def main():
    print("=== YouTube OAuth2 Refresh Token Generator ===")
    print("Please make sure you have added 'http://localhost:8080/' as an Authorized Redirect URI in your Google Cloud Console Credentials.")
    client_id = input("\nEnter your Client ID: ").strip()
    client_secret = input("Enter your Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("Error: Client ID and Client Secret are required.")
        sys.exit(1)
        
    scopes = "https://www.googleapis.com/auth/yt-analytics.readonly https://www.googleapis.com/auth/youtube.readonly"
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        f"&scope={scopes}"
        "&access_type=offline"
        "&prompt=consent"
    )
    
    # Start temporary local HTTP server
    server = HTTPServer(("localhost", PORT), OAuthRedirectHandler)
    
    print("\nOpening your browser to authorize access to YouTube Analytics...")
    webbrowser.open(auth_url)
    
    print("Waiting for callback on http://localhost:8080/ ...")
    server.handle_request() # Wait for a single request
    server.server_close()
    
    if auth_code:
        print("\nExchanging authorization code for tokens...")
        try:
            tokens = get_tokens(client_id, client_secret, auth_code)
            print("\n=== SUCCESS ===")
            print(f"Refresh Token: {tokens.get('refresh_token')}")
            print("\nSave this Refresh Token and add it to your .env / Vercel Environment Variables.")
        except Exception as e:
            print(f"\nError: {e}")
    else:
        print("\nError: Did not receive authorization code.")

if __name__ == "__main__":
    main()
