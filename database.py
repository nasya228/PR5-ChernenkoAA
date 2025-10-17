import sqlite3
from typing import Optional, List

class Database:
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
