from db.db_context import DatabaseContext
from datetime import datetime

class FuelRepsitory:
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

    def insert_fuel_data(self, fuel_data: list):
        """Insert fuel prices into the database"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        insert_query = '''
        INSERT INTO fuel_prices (date, provider, type, price)
        VALUES (%s, %s, %s, %s)
        '''
        
        for entry in fuel_data:
            self.db_manager.execute(insert_query, (current_date, entry['provider'], entry['type'], entry['price']))
        print(f"Fuel data inserted successfully.")
