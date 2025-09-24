from get_data import get_data_from_db
import config

db_path=config.db_path
output_file=config.output_file
 
if __name__ == "__main__":
    df=get_data_from_db(db_path)
    df['total_quantity'] = df['total_quantity'].astype(int)
    if not df.empty:
        df.rename(columns={
            'customer_id': 'Customer',
            'age': 'Age',
            'item_name': 'Item',
            'quantity': 'Quantity'
        }, inplace=True)
        
        df.to_csv(output_file, sep=';', index=False)
        
    else:
        print("No data to save.")
