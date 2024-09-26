from app.errors.handlers import DatabaseException, error_types
from db.db_context import DatabaseContext
from datetime import datetime


class FuelRepository:
    def __init__(self, db_manager: DatabaseContext):
        """Initialize with a reference to the generic Repsitory"""
        self.db_manager = db_manager

    def create_fuel_table(self):
        """Create table for storing fuel data if it doesn't exist"""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS fuel_prices (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            provider VARCHAR(50),
            type VARCHAR(50),
            price NUMERIC(10, 2)
        );
        '''
        self.db_manager.execute(create_table_query)

    def insert_fuel_data(self, fuel_data: list, provider: str):
        """Insert fuel prices into the database, but first check if data for the current date already exists."""
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Query to check if data for the current date already exists
        check_query = '''
        SELECT 1 FROM fuel_prices
        WHERE date = %s AND
        provider = %s
        LIMIT 1
        '''

        result = self.db_manager.fetchone(check_query, (current_date, provider,))  # Fetch one result from the query

        if result:  # If the result is not empty, data exists
            raise DatabaseException(
                error_type=error_types['conflict']['type'],
                message=f"Data for {current_date} already exists in the database."
            )
        else:
            # Insert the new data if no data for the current date exists
            insert_query = '''
            INSERT INTO fuel_prices (date, provider, type, price)
            VALUES (%s, %s, %s, %s)
            '''
            for entry in fuel_data:
                self.db_manager.execute(
                    insert_query, (current_date, entry['provider'], entry['type'], entry['price']))

    def get_fuel_prices(self, fuel_type=('แก๊สโซฮอล์ 95', 'แก๊สโซฮอล์ E20', 'ดีเซล B7')):
        today_date = datetime.now().strftime('%Y-%m-%d')

        query = """
        SELECT provider, type, price
        FROM fuel_prices
        WHERE type IN %s
        AND date = %s
        ORDER BY provider, type;
        """

        rows = self.db_manager.fetchall(query, (fuel_type, today_date,))
        return rows
