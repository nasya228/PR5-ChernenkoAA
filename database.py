import sqlite3
from typing import Optional, List
def example_usage():
    """Пример использования базы данных"""
    with Database("example.db") as db:
        db.create_tables()
        
     
        user_id = db.create_user("alex", "alex@example.com", "secure_hash")
        print(f"Создан пользователь с ID: {user_id}")
        
     
        user = db.get_user_by_id(user_id)
        print("Данные пользователя:", user)
        
        
        db.update_user_settings(user_id, "dark", "en", True)
        
      
        settings = db.get_user_settings(user_id)
        print("Настройки пользователя:", settings)

if __name__ == "__main__":
    example_usage()

class Database:
            def get_user_settings(self, user_id: int) -> Optional[dict]:
        """Получение настроек пользователя"""
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM settings WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                'user_id': row[0],
                'theme': row[1],
                'language': row[2],
                'notifications': bool(row[3])
            }
        return None

    def backup_database(self, backup_path: str) -> bool:
        """Создание резервной копии базы данных"""
        try:
            import shutil
            shutil.copy2(self.db_name, backup_path)
            print(f"резервная копия создана: {backup_path}")
            return True
        except Exception as e:
            print(f"ошибка создания резервной копии: {e}")
            return False

    def __enter__(self):
        """Поддержка контекстного менеджера"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие соединения"""
        self.close()
            
        def authenticate_user(self, username: str, password_hash: str) -> Optional[dict]:
        """Аутентификация пользователя"""
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'created_at': row[4]
            }
        return None

    def update_user_settings(self, user_id: int, theme: str, language: str, notifications: bool) -> bool:
        """Обновление настроек пользователя"""
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        try:
      
            cursor.execute("DELETE FROM settings WHERE user_id = ?", (user_id,))
            
    
            cursor.execute(
                "INSERT INTO settings (user_id, theme, language, notifications) VALUES (?, ?, ?, ?)",
                (user_id, theme, language, 1 if notifications else 0)
            )
            self.connection.commit()
            print(f"настройки пользователя {user_id} обновлены")
            return True
        except sqlite3.Error as e:
            print(f"ошибка обновления настроек: {e}")
            return False
            
    def __init__(self, db_name: str = "app_database.db"):
        self.db_name = db_name
        self.connection: Optional[sqlite3.Connection] = None
    
    def connect(self) -> None:
        """Установка соединения с базой данных"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            print("подключение к базе данных установлено")
        except sqlite3.Error as e:
            print(f"ошибка подключения: {e}")
    
    def create_tables(self) -> None:
        """создание необходимых таблиц"""
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        
     
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
      
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                user_id INTEGER,
                theme TEXT DEFAULT 'light',
                language TEXT DEFAULT 'ru',
                notifications INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.connection.commit()
        print("таблицы созданы успешно")
           

    def create_user(self, username: str, email: str, password_hash: str) -> int:
        """Создание нового пользователя"""
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            self.connection.commit()
            print(f"пользователь {username} создан")
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise DuplicateUserError(f"Пользователь {username} или {email} уже существует") from e

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """Получение пользователя по ID"""
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'password_hash': row[3],
                'created_at': row[4]
            }
        return None

class DatabaseError(Exception):
    """Базовое исключение для ошибок базы данных"""
    pass

class UserNotFoundError(DatabaseError):
    """Пользователь не найден"""
    pass

class DuplicateUserError(DatabaseError):
    """Пользователь с таким именем или email уже существует"""
    pass
