import psycopg2
from my_env import db_params

class DatabaseContext:
    def __init__(self):
        self.db_params = db_params
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to the PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**self.db_params)
            self.cursor = self.conn.cursor()
        except psycopg2.DatabaseError as e:
            print(f"Error connecting to the database: {e}")
            raise

    def close(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute(self, query: str, params=None):
        """Execute a query on the database"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            self.conn.rollback()
            raise
    
    def fetchall(self, query, params=None):
        """Fetch all results from a query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        """Fetch a single result from a query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()