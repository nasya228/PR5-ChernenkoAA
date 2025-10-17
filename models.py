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
        def validate_user_data(username: str, email: str, password: str) -> list:
    """
    Валидация данных пользователя
    
    Returns:
        list: список ошибок, пустой если ошибок нет
    """
    errors = []
    
    if len(username) < 3:
        errors.append("Имя пользователя должно быть не менее 3 символов")
    
    if len(username) > 50:
        errors.append("Имя пользователя должно быть не более 50 символов")
    
    if '@' not in email:
        errors.append("Некорректный email адрес")
    
    if len(password) < 6:
        errors.append("Пароль должен быть не менее 6 символов")
    
    return errors

def hash_password(password: str) -> str:
    """
    Хеширование пароля (упрощенная версия)
    
    В реальном приложении используйте bcrypt или аналоги
    """
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


if __name__ == "__main__":
    
    user = User("test_user", "test@example.com", "hashed_password")
    print("Создан пользователь:", user.to_dict())
    
    settings = UserSettings(1, "dark", "en", False)
    print("Настройки пользователя:", settings.to_dict())
