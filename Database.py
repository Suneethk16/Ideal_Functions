import pandas as pd
from sqlalchemy import create_engine
from Exceptions import DataLoadError

class database:
    """
    Uses SQLAlchemy to manage database activities, including data reading and writing.
    """
    def __init__(self, db_name="sqlite:///functions.db"):
        """
        Uses a SQLite database to initialize the database handler.
        """
        self.engine = create_engine(db_name)

    def load_to_database(self, df: pd.DataFrame, table_name: str):
        """
        Loads a DataFrame into a designated database table.
        If a problem occurs when writing to the database, it raises the DataLoadError.
        """
        try:
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
        except Exception as e:
            raise DataLoadError(f"Failed to load data to {table_name}: {e}")
