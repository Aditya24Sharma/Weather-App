import duckdb
import pandas as pd

def checkZipCode(zip_code):
    file_path = 'Zip_codes_with_location.csv'
    # abs_file_path = os.path.normpath(file_path)
    query = f"""
    SELECT * FROM '{file_path}' as 'dataset'   
    WHERE zip = {int(zip_code)}
        """
    sql = duckdb.sql(query)
    if not sql:
        return False 

    return True

if __name__ == '__main__':
    checkZipCode('01180')
    