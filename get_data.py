import pandas as pd
from sql_connection import get_connection

'''This Function contains data extraction & transformation logic 
input: database path
output: dataframe
'''
def get_data_from_db(db_path):
    conn = None
    try:
        conn = get_connection(db_path)        
        if conn is None:
            return pd.DataFrame()
           
        try:            
            df_orders = pd.read_sql_query("SELECT * FROM Orders", conn)
            df_sales = pd.read_sql_query("SELECT * FROM Sales", conn)
            df_customer = pd.read_sql_query("SELECT * FROM Customer", conn)
            df_items = pd.read_sql_query("SELECT * FROM Items", conn)
        except pd.io.sql.DatabaseError as e:
            print(f"Error reading tables from database: {e}")
            return pd.DataFrame()
        finally:
            conn.close()        
            
        customers_age_filtered = df_customer[(df_customer['age'] >= 18) & (df_customer['age'] <= 35)].copy()
        sales_customer = pd.merge(df_sales, customers_age_filtered, on='customer_id')
        orders_sales_customer = pd.merge(df_orders, sales_customer, on='sales_id')
        final_df = pd.merge(orders_sales_customer, df_items, on='item_id')
        final_df = final_df.dropna(subset=['quantity'])
        grouped_df = final_df.groupby(['customer_id', 'age', 'item_name'])['quantity'].sum().reset_index()
        grouped_df = grouped_df[grouped_df['quantity'] > 0]
        grouped_df['quantity'] = grouped_df['quantity'].astype(int)

        return grouped_df    
    
    except Exception as e:
        print(f"Error : {e}")

