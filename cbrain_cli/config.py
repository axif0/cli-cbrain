"""
CBRAIN CLI Configuration
"""

from pathlib import Path

# Default settings.
DEFAULT_BASE_URL = "http://localhost:3000"

# Session file configuration.
SESSION_FILE_DIR = Path.home() / ".config" / "cbrain"
SESSION_FILE_NAME = "credentials.json"
SESSION_FILE_DIR.mkdir(parents=True, exist_ok=True) 

# HTTP headers.
DEFAULT_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}
 
