import psycopg2
import asyncio
import config


class DBDConnector:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD,
                                     host=config.DB_HOST, port=config.DB_PORT)
        self.cursor = self.conn.cursor()

    async def create_table_users(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY
        )""")
        self.conn.commit()

    async def create_table_tasks(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        task TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        )""")
        self.conn.commit()

    async def add_user(self, user_id):
        self.cursor.execute(f"SELECT user_id FROM users WHERE user_id={user_id}")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"INSERT INTO users (user_id) VALUES ({user_id})")
            self.conn.commit()

    async def get_user_tasks(self, user_id):
        self.cursor.execute(f"SELECT task FROM tasks WHERE user_id={user_id}")
        tasks = self.cursor.fetchall()
        return tasks

    async def add_task(self, user_id, task):
        self.cursor.execute("INSERT INTO tasks (user_id, task) VALUES (%s, %s)", (user_id, task))
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

# Раскоментировать для создания таблиц в БД.
# db = DBDConnector()
# asyncio.run(db.create_table_users())
# asyncio.run(db.create_table_tasks())
