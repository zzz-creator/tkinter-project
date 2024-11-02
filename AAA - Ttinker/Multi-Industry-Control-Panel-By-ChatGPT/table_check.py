import pyodbc

# Connection function (update with your connection details)
server = 'localhost'  # e.g. 'localhost' or 'your_server_name'
database = 'MultiIndustryControlPanel'
username = 'admin'
password = 'admin'

# Function to connect to the database
def connect_db():
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;'
    print(conn_str)
    return pyodbc.connect(conn_str)
    

# List of tables to check
tables_to_check = ["AerospaceData", "IndustrialData", "TransportationData", "ResearchData", "MaritimeData"]

# Function to get and display columns for each table
def get_table_columns():
    conn = connect_db()
    cursor = conn.cursor()
    
    for table_name in tables_to_check:
        print(f"\nColumns in table '{table_name}':")
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", (table_name,))
        columns = [row.COLUMN_NAME for row in cursor.fetchall()]
        
        if columns:
            print(columns)
        else:
            print("Table does not exist or has no columns.")
    
    cursor.close()
    conn.close()

# Call the function to display columns
get_table_columns()
