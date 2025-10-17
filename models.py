from datetime import datetime
from typing import Optional

class User:
    
    
    def __init__(self, username: str, email: str, password_hash: str, user_id: Optional[int] = None):
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
       
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        
        user = cls(
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            user_id=data.get('id')
        )
        if data.get('created_at'):
            user.created_at = datetime.fromisoformat(data['created_at'])
        return user

class UserSettings:
  
    
    def __init__(self, user_id: int, theme: str = 'light', language: str = 'ru', notifications: bool = True):
        self.user_id = user_id
        self.theme = theme
        self.language = language
        self.notifications = notifications
    
    def to_dict(self) -> dict:
        
        return {
            'user_id': self.user_id,
            'theme': self.theme,
            'language': self.language,
            'notifications': self.notifications
        }
