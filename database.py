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
