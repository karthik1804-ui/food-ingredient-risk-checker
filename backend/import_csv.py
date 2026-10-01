import sqlite3
import pandas as pd

def import_csv():
    csv_path = r"D:\food-risk-checker\backend\additives.csv"
    db_path = "additives.db"
    
    print(f"Reading CSV from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Standardize high_risk_flag to 1 (True) or 0 (False)
    print("Normalizing high_risk_flag column...")
    df['high_risk_flag'] = df['high_risk_flag'].map({
        'TRUE': 1, 'FALSE': 0,
        'True': 1, 'False': 0,
        '1': 1, '0': 0,
        True: 1, False: 0,
        1: 1, 0: 0
    }).fillna(0).astype(int)
    
    # Re-order/select columns to ensure schema aligns
    columns = [
        'id', 'code', 'ins_number', 'additive_name', 
        'category', 'description', 'risk_score', 
        'high_risk_flag', 'risk_score_reason'
    ]
    df = df[columns]

    print(f"Connecting to SQLite database {db_path}...")
    conn = sqlite3.connect(db_path)
    
    print("Storing data into 'additives' table...")
    df.to_sql(
        "additives",
        conn,
        if_exists="replace",
        index=False
    )
    
    conn.close()
    print("CSV imported successfully into SQLite DB!")

if __name__ == "__main__":
    import_csv()