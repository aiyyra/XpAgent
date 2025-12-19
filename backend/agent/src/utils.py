
import re
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
    
def correct_malformed_json(malformed_json_string):
    # Step 1: Replace escaped quotes with actual quotes
    corrected_json_string = malformed_json_string.replace('\\"', '"')

    # Step 2: Ensure all keys and values are properly closed
    # This regular expression will find unquoted strings and put quotes around them
    # It skips already quoted values and datetime formats
    def quote_value(match):
        value = match.group(1)
        if not re.match(r'^".*"$', value) and not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', value):
            value = f'"{value}"'
        return value
    
    corrected_json_string = re.sub(r':(\w+)', quote_value, corrected_json_string)

    # Step 3: Handle duplicate keys by making them unique
    seen_keys = set()
    def make_unique(match):
        key = match.group(1)
        if key in seen_keys:
            counter = 2
            new_key = f"{key}{counter}"
            while new_key in seen_keys:
                counter += 1
                new_key = f"{key}{counter}"
            key = new_key
        seen_keys.add(key)
        return f'"{key}"'
    
    corrected_json_string = re.sub(r'"(\w+)"(?=:)', make_unique, corrected_json_string) 

    # Step 4: Add missing closinf brace if needed
    if corrected_json_string.count('{') > corrected_json_string.count('}'):
        corrected_json_string += '}'
    
    return corrected_json_string



