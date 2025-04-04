import os
import json
import requests
from pathlib import Path

class CBRAINSession:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.session_file = Path.home() / ".cbrain" / "session.json"
        self.token = None
        self.user_id = None
        self._load_session()

    def _load_session(self):
         
        if self.session_file.exists():
            try:
                with open(self.session_file) as f:
                    data = json.load(f)
                    self.token = data.get('cbrain_api_token')
                    self.user_id = data.get('user_id')
            except (json.JSONDecodeError, IOError) as e:
                self.token = None
                self.user_id = None
        else:
            pass

    def _verify_token(self):
       
        if not self.token:
            return False
            
        url = f"{self.base_url}/session"
        headers = self.get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            valid = response.status_code == 200
            return valid
        except requests.exceptions.RequestException as e:
            return False

    def _save_session(self):
         
        try:
            self.session_file.parent.mkdir(exist_ok=True)
            data = {
                'cbrain_api_token': self.token,
                'user_id': self.user_id
            }
            with open(self.session_file, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            pass

    def login(self, username, password):
     
        url = f"{self.base_url}/session"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        payload = f'login={username}&password={password}'

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            
            # Extract token from response body
            data = response.json()
            self.token = data.get('cbrain_api_token')
            self.user_id = data.get('user_id')
            
            if self.token:
                self._save_session()
                return True
            return False
        except requests.exceptions.RequestException as e:
            return False

    def get_headers(self):
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}' if self.token else None
        }
        return headers

    def is_authenticated(self):
       
        is_auth = bool(self.token)
        return is_auth

    def logout(self):
        """Clear the current session."""
        if self.session_file.exists():
            try:
                self.session_file.unlink()
            except IOError as e:
                pass
        self.token = None
        self.user_id = None 