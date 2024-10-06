import pandas as pd
import pyodbc

# Define your connection string
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
csv_file_path = './13f_filings_summary.csv'  # Update with the path to your CSV file
df = pd.read_csv(csv_file_path)
# Ensure that the data types match the SQL table schema
df['FileNumber'] = df['FileNumber'].astype(str)
df['FileType'] = df['FileType'].astype(str)
df['Filename'] = df['Filename'].astype(str)
df['Description'] = df['Description'].astype(str)
df['ReportDate'] = pd.to_datetime(df['ReportDate'], errors='coerce')  # Ensure correct date format
df['CompanyName'] = df['CompanyName'].astype(str)
df['PersonName'] = df['PersonName'].astype(str)
df['Title'] = df['Title'].astype(str)
df['Phone'] = df['Phone'].astype(str)
df['Signature'] = df['Signature'].astype(str)
df['ReportType'] = df['ReportType'].astype(str)
df['Address'] = df['Address'].astype(str)
df['NumberOfOtherIncludedManagers'] = pd.to_numeric(df['NumberOfOtherIncludedManagers'], errors='coerce')
df['InformationTableEntryTotal'] = pd.to_numeric(df['InformationTableEntryTotal'], errors='coerce')
df['InformationTableValueTotal'] = df['InformationTableValueTotal'].astype(str)
df['ListOfOtherIncludedManagers'] = df['ListOfOtherIncludedManagers'].astype(str)
df['InformationTable'] = df['InformationTable'].astype(str)

# Iterate over DataFrame rows and insert them into the database
for index, row in df.iterrows():
    cursor.execute('''
        INSERT INTO ReportFiles (FileNumber, FileType, Filename, Description, ReportDate, 
                                 CompanyName, PersonName, Title, Phone, Signature, 
                                 ReportType, Address, NumberofOtherIncludedManagers, 
                                 InformationTableEntryTotal, InformationTableValueTotal, 
                                 ListOfOtherIncludedManagers, InformationTable)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        row['FileNumber'], row['FileType'], row['Filename'], row['Description'], row['ReportDate'],
        row['CompanyName'], row['PersonName'], row['Title'], row['Phone'], row['Signature'],
        row['ReportType'], row['Address'], row['NumberOfOtherIncludedManagers'], 
        row['InformationTableEntryTotal'], row['InformationTableValueTotal'], 
        row['ListOfOtherIncludedManagers'], row['InformationTable']
    )

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()
