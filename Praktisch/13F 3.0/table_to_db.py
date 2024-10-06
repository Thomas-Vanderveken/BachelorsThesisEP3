import pandas as pd
import pyodbc

# Database connection details
conn_str = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=DESKTOP-FD4KP8N;"
    "DATABASE=FinancialReports;"
    "Trusted_Connection=yes;"
)
# Establish a connection to the database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


# Read CSV data into a DataFrame
csv_file_path = './13F_IT_cleaned.csv'  # Update with the path to your CSV file
df = pd.read_csv(csv_file_path)

# Ensure correct data types for each column
df['Shares'] = pd.to_numeric(df['Shares'], errors='coerce')
df['MarketValue(in$1000)'] = pd.to_numeric(df['MarketValue(in$1000)'], errors='coerce')
df['VotingAuthority(Sole)'] = pd.to_numeric(df['VotingAuthority(Sole)'], errors='coerce')
df['VotingAuthority(Shared)'] = pd.to_numeric(df['VotingAuthority(Shared)'], errors='coerce')
df['VotingAuthority(None)'] = pd.to_numeric(df['VotingAuthority(None)'], errors='coerce')

# Iterate over DataFrame rows and insert them into the database
for index, row in df.iterrows():
    try:
        cursor.execute('''
            INSERT INTO InvestmentDetails (
                FileNumber, SecurityDescription, Class, CUSIP, Shares, MarketValueInThousands, 
                InvestmentDiscretion, VotingAuthoritySole, VotingAuthorityShared, VotingAuthorityNone
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            row['FileNumber'],row['SecurityDescription'],row['Class'],row['CUSIP'],
            row['Shares'],row['MarketValue(in$1000)'],row['InvestmentDiscretion'],
            row['VotingAuthority(Sole)'],row['VotingAuthority(Shared)'],
            row['VotingAuthority(None)']
        )
    except pyodbc.Error as e:
        print(f"Error inserting row {index}: {e}")

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data inserted successfully!")
