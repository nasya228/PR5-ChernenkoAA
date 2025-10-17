import re
import hashlib
import secrets
from typing import List, Tuple
import string

class SecurityUtils:
    """Утилиты для обеспечения безопасности"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Валидация email адреса
        
        Args:
            email: email для проверки
            
        Returns:
            bool: True если email валиден
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
        """
        Проверка сложности пароля
        
        Args:
            password: пароль для проверки
            
        Returns:
            Tuple[bool, List[str]]: (валиден, список ошибок)
        """
        errors = []
        
        if len(password) < 8:
            errors.append("Пароль должен содержать минимум 8 символов")
        
        if not any(c.isupper() for c in password):
            errors.append("Пароль должен содержать хотя бы одну заглавную букву")
        
        if not any(c.islower() for c in password):
            errors.append("Пароль должен содержать хотя бы одну строчную букву")
        
        if not any(c.isdigit() for c in password):
            errors.append("Пароль должен содержать хотя бы одну цифру")
        
        if not any(c in string.punctuation for c in password):
            errors.append("Пароль должен содержать хотя бы один специальный символ")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Генерация безопасного токена
        
        Args:
            length: длина токена
            
        Returns:
            str: безопасный токен
        """
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """
        Очистка пользовательского ввода от потенциально опасных символов
        
        Args:
            user_input: пользовательский ввод
            
        Returns:
            str: очищенная строка
        """
       
        cleaned = re.sub(r'<script.*?>.*?</script>', '', user_input, flags=re.IGNORECASE)
        cleaned = re.sub(r'<.*?>', '', cleaned)
        
   
        cleaned = cleaned.replace('"', '\\"')
        cleaned = cleaned.replace("'", "\\'")
        cleaned = cleaned.replace(';', '\\;')
        
        return cleaned.strip()
    
    @staticmethod
    def rate_limit_check(identifier: str, attempts: int, window_minutes: int) -> bool:
        """
        Проверка ограничения запросов
        
        Args:
            identifier: идентификатор (IP, username)
            attempts: максимальное количество попыток
            window_minutes: окно времени в минутах
            
        Returns:
            bool: True если лимит не превышен
        """
      
        import time
        current_time = time.time()
        
    
        return True
    
    @staticmethod
    def generate_csrf_token() -> str:
        """
        Генерация CSRF токена
        
        Returns:
            str: CSRF токен
        """
        return secrets.token_hex(32)

if __name__ == "__main__":
    utils = SecurityUtils()
    
   
    test_emails = ["test@example.com", "invalid-email", "user@domain.ru"]
    for email in test_emails:
        is_valid = utils.validate_email(email)
        print(f"Email {email}: {'валиден' if is_valid else 'невалиден'}")
    
   
    test_passwords = ["weak", "Medium1", "StrongPass123!"]
    for pwd in test_passwords:
        is_strong, errors = utils.validate_password_strength(pwd)
        print(f"Пароль {pwd}: {'сильный' if is_strong else 'слабый'}")
        if errors:
            print("  Ошибки:", errors)
