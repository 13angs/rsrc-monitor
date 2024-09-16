import psycopg2

class DatabaseContext:
    def __init__(self, db_params: dict):
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