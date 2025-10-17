import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict

class AuthSystem:
    """Система аутентификации пользователей"""
    def track_failed_attempt(self, username: str) -> bool:
        """
        Отслеживание неудачных попыток входа
        
        Args:
            username: имя пользователя
            
        Returns:
            bool: True если аккаунт не заблокирован
        """
        if username not in self.failed_attempts:
            self.failed_attempts[username] = {
                'count': 0,
                'first_attempt': datetime.now()
            }
        
        self.failed_attempts[username]['count'] += 1
        self.failed_attempts[username]['last_attempt'] = datetime.now()
        
      
        if self.failed_attempts[username]['count'] >= 5:
            time_since_first = datetime.now() - self.failed_attempts[username]['first_attempt']
            if time_since_first < timedelta(minutes=15):
                return False
        
        return True
    
    def reset_failed_attempts(self, username: str) -> None:
        """Сброс счетчика неудачных попыток"""
        if username in self.failed_attempts:
            del self.failed_attempts[username]
    
    def is_account_locked(self, username: str) -> bool:
        """Проверка заблокирован ли аккаунт"""
        if username not in self.failed_attempts:
            return False
        
        attempts = self.failed_attempts[username]
        if attempts['count'] >= 5:
            time_since_first = datetime.now() - attempts['first_attempt']
            return time_since_first < timedelta(minutes=15)
        
        return False
        
        def create_session(self, user_id: int, username: str) -> str:
        """
        Создание сессии пользователя
        
        Args:
            user_id: ID пользователя
            username: имя пользователя
            
        Returns:
            str: ID сессии
        """
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            'user_id': user_id,
            'username': username,
            'created_at': datetime.now(),
            'last_activity': datetime.now()
        }
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[dict]:
        """
        Проверка валидности сессии
        
        Args:
            session_id: ID сессии
            
        Returns:
            dict: данные сессии или None
        """
        session = self.sessions.get(session_id)
        if not session:
            return None
        
       
        if datetime.now() - session['created_at'] > timedelta(hours=24):
            del self.sessions[session_id]
            return None
        
       
        session['last_activity'] = datetime.now()
        return session
    
    def destroy_session(self, session_id: str) -> bool:
        """
        Удаление сессии
        
        Args:
            session_id: ID сессии
            
        Returns:
            bool: True если сессия удалена
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    def __init__(self):
        self.sessions = {}
        self.failed_attempts = {}
    
    def hash_password(self, password: str) -> str:
        """
        Хеширование пароля с солью
        
        Args:
            password: пароль в открытом виде
            
        Returns:
            str: хеш пароля с солью
        """
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000 
        )
        return f"{salt}${password_hash.hex()}"
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Проверка пароля
        
        Args:
            password: пароль для проверки
            hashed_password: хеш из базы данных
            
        Returns:
            bool: True если пароль верный
        """
        try:
            salt, stored_hash = hashed_password.split('$')
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return new_hash.hex() == stored_hash
        except ValueError:
            return False
