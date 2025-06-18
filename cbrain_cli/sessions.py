import json
import urllib.request
import urllib.parse
import urllib.error
import getpass
from cbrain_cli.config import (
    DEFAULT_BASE_URL, SESSION_FILE_DIR, SESSION_FILE_NAME, DEFAULT_HEADERS
)

def create_session(args):
    """
    Create a new CBRAIN session by logging in and saving credentials.

    Returns
    -------
    None
        A command is ran via inputs from the user.
    """
    credentials_file = SESSION_FILE_DIR / SESSION_FILE_NAME
    if credentials_file.exists():
        print("Already logged in. Use 'cbrain logout' to logout.")
        return 1
     
    # Get user input.
    cbrain_url = input("Enter CBRAIN server URL prefix: ").strip()
    if not cbrain_url:
        cbrain_url = DEFAULT_BASE_URL
        
    username = input("Enter CBRAIN username: ").strip()
    if not username:
        print("Username is required")
        return 1
        
    password = getpass.getpass("Enter CBRAIN password: ")
    if not password:
        print("Password is required")
        return 1

    # Prepare the login request.
    login_endpoint = f"{cbrain_url}/session"
    
    # Prepare form data.
    form_data = {
        'login': username,
        'password': password
    }
    
    # Encode the form data.
    encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
    
    # Create the request.
    request = urllib.request.Request(
        login_endpoint,
        data=encoded_data,
        headers=DEFAULT_HEADERS,
        method='POST'
    )
    
    # Make the request.
    with urllib.request.urlopen(request) as response:
        data = response.read().decode('utf-8')
        response_data = json.loads(data)
        
        # Extract the API token from response.
        cbrain_api_token = response_data.get('cbrain_api_token')  
        cbrain_user_id = response_data.get('cbrain_user_id')
        
        if not cbrain_api_token:
            print("Login failed: No API token received")
            return 1
            
        # Prepare credentials data.
        credentials = {
            'cbrain_url': cbrain_url,
            'api_token': cbrain_api_token,
            'user_id': cbrain_user_id
        }
        
        # Save credentials to file.
        with open(credentials_file, 'w') as f:
            json.dump(credentials, f, indent=2)
            
        print(f"Connection successful, API token saved in {credentials_file}")
        return 0