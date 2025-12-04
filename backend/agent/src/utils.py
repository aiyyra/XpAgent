
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

def _get_db_schema(db_path, tables=None, sample_rows_in_table_info=5):
    
    # Initializes the database connection
    engine = create_engine(f'sqlite:///{db_path}') # we will use the ArtWork sqlite Database for this case
    database = SQLDatabase(engine, sample_rows_in_table_info=sample_rows_in_table_info)
    
    # List of tables you want the schema for
    if tables is None:
        db_schema = database.get_table_info()
    db_schema = database.get_table_info(tables)

    return db_schema
    