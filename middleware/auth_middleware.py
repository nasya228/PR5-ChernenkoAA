import jwt
from datetime import datetime, timedelta
from typing import Optional, Callable, Any
import secrets

class AuthMiddleware:
    """Middleware для обработки аутентификации"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = 'HS256'
    
    def generate_token(self, user_id: int, username: str, expires_hours: int = 24) -> str:
        """
        Генерация JWT токена
        
        Args:
            user_id: ID пользователя
            username: имя пользователя
            expires_hours: срок действия в часах
            
        Returns:
            str: JWT токен
        """
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=expires_hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[dict]:
        """
        Проверка JWT токена
        
        Args:
            token: JWT токен
            
        Returns:
            dict: payload токена или None если невалидный
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            print("Токен истек")
            return None
        except jwt.InvalidTokenError:
            print("Невалидный токен")
            return None
    
    def require_auth(self, func: Callable) -> Callable:
        """
        Декоратор для защиты функций аутентификацией
        
        Args:
            func: функция для защиты
            
        Returns:
            Callable: обернутая функция
        """
        def wrapper(*args, **kwargs):
            token = kwargs.get('token') or (args[0] if args else None)
            if not token:
                return {'error': 'Токен отсутствует'}, 401
            
            payload = self.verify_token(token)
            if not payload:
                return {'error': 'Невалидный токен'}, 401
            
            kwargs['user'] = payload
            return func(*args, **kwargs)
        
        return wrapper
    
    def check_permission(self, required_permission: str) -> Callable:
        """
        Декоратор для проверки прав доступа
        
        Args:
            required_permission: требуемое право
            
        Returns:
            Callable: декоратор
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                user = kwargs.get('user')
                if not user:
                    return {'error': 'Пользователь не аутентифицирован'}, 401
              
                user_permissions = user.get('permissions', [])
                
                if required_permission not in user_permissions:
                    return {'error': 'Недостаточно прав'}, 403
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
