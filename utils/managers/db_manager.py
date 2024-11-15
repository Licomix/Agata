#From https://github.com/flacsy/BotArchitecture

import logging
import aiosqlite

class SQLiteDatabaseManager:
    def __init__(self):
        """
        Параметр `mode` это режим для базы данных. Возможные значения: 'development' для розроботки, 'production' для продакшина
        """
        self.conn = None
        self.cursor = None

    async def __aenter__(self):
        try:
            self.conn = await aiosqlite.connect("./utils/databases/database.sqlite")
            self.cursor = await self.conn.cursor()
            logging.info(f"Connected to the database")
            return self.cursor
        except aiosqlite.Error as e:
            logging.error(f"Error connecting to the database: {e}")
            raise

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            await self.cursor.close()
            logging.info("Cursor closed")
        if self.conn:
            await self.conn.commit()
            await self.conn.close()
            logging.info("Connection closed")

        if exc_type is not None:
            logging.error(f"An error occurred: {exc_type}, {exc_value}")

        return False

async def create_table():
    async with SQLiteDatabaseManager() as conn:
        await conn.execute("""CREATE TABLE IF NOT EXISTS user_messages (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                message_count INTEGER
            );
        """)
