import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict

class AuthSystem:
    """Система аутентификации пользователей"""
    
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
