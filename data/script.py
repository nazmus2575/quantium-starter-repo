import csv
import os

# Step 1: List all 3 input files
input_files = [
    "daily_sales_data_0.csv",
    "daily_sales_data_1.csv",
    "daily_sales_data_2.csv",
]

output_rows = []

# Step 2: Loop through each file and process rows
for filepath in input_files:
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)  # reads each row as a dictionary
        for row in reader:

            # Filter: keep ONLY pink morsel rows
            if row['product'].strip().lower() != 'pink morsel':
                continue  # skip this row entirely

            # Calculate sales = price × quantity
            price = float(row['price'].replace('$', ''))  # remove the "$" sign first
            quantity = int(row['quantity'])
            sales = price * quantity

            # Keep only the 3 fields we need
            output_rows.append({
                'sales': sales,
                'date': row['date'],
                'region': row['region']
            })

# Step 3: Write everything into one output file
with open('daily_sales_data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['sales', 'date', 'region'])
    writer.writeheader()  # writes the column names
    writer.writerows(output_rows)  # writes all the data rows