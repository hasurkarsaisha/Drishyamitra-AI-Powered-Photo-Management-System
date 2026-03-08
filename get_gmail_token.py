"""
Generate Gmail OAuth refresh token
Run this once to get your refresh token
"""
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Scopes required for Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_refresh_token():
    """Generate refresh token for Gmail API"""
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("\nCreate credentials.json with your OAuth client credentials:")
        print("""
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token"
  }
}
        """)
        return
    
    creds = None
    
    # Check if token.pickle exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Use port 8080 to match redirect URI
            creds = flow.run_local_server(port=8080)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    print("\n✅ Success! Your refresh token:")
    print(f"\n{creds.refresh_token}\n")
    print("Add this to your .env file:")
    print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
    print(f"\nAlso add:")
    print(f"GMAIL_CLIENT_ID=<your_client_id>")
    print(f"GMAIL_CLIENT_SECRET=<your_client_secret>")

if __name__ == '__main__':
    try:
        get_refresh_token()
    except ImportError:
        print("❌ Missing dependencies!")
        print("\nInstall with:")
        print("pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
