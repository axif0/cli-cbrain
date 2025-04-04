import requests
from typing import Dict, Optional

class UserManager:
    def __init__(self, session):
        self.session = session

    def create_user(self, user_data: Dict) -> Optional[Dict]:
        url = f"{self.session.base_url}/users"
        
        payload = {
            "user": {
                "login": user_data['login'],
                "password": user_data['password'],
                "password_confirmation": user_data['password'],
                "full_name": user_data['full_name'],
                "email": user_data['email'],
                "city": user_data.get('city', ''),
                "country": user_data.get('country', ''),
                "time_zone": user_data.get('time_zone', 'UTC'),
                "type": user_data.get('type', 'NormalUser'),
                "site_id": user_data.get('site_id', 1)
            },
            "no_password_reset_needed": 1,
            "force_password_reset": False
        }

        try:
            response = requests.post(
                url,
                headers=self.session.get_headers(),
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def list_users(self) -> Optional[list]:
       
        url = f"{self.session.base_url}/users"
        
        try:
            response = requests.get(
                url,
                headers=self.session.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def get_user(self, user_id: int) -> Optional[Dict]:
      
        url = f"{self.session.base_url}/users/{user_id}"
        
        try:
            response = requests.get(
                url,
                headers=self.session.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None 