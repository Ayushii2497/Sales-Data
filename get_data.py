import pandas as pd
from sql_connection import get_connection

'''This Function contains data extraction & transformation logic 
input: database path
output: dataframe
'''
def get_data_from_db(db_path):
    conn = None
    try:
        """
        Extracts total quantities of each item for customers aged 18-35 using a single SQL query.
        """
        conn = get_connection(db_path)
        if conn is None:
            return pd.DataFrame()

        query = """
        SELECT
            t2.customer_id,
            t2.age,
            t4.item_name,
            SUM(t1.quantity) AS total_quantity
        FROM
            Orders AS t1
        JOIN
            Sales AS t3 ON t1.sales_id = t3.sales_id
        JOIN
            Customer AS t2 ON t3.customer_id = t2.customer_id
        JOIN
                Items AS t4 ON t1.item_id = t4.item_id
            WHERE
                t2.age BETWEEN 18 AND 35
                AND t1.quantity IS NOT NULL
            GROUP BY
                t2.customer_id,
                t2.age,
                t4.item_name
            HAVING
                SUM(t1.quantity) > 0;
            """
        try:
            df = pd.read_sql_query(query, conn)
            return df
        except pd.io.sql.DatabaseError as e:
            print(f"Error executing SQL query: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    
    except Exception as e:
        print(f"Error : {e}")

