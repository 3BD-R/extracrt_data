import pandas as pd
import sys


def main(file_path):
    try:
        data_file = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Clean and standardize column names
    data_file.columns = data_file.columns.str.strip()
    required_columns = ['Courier Name', 'Status', 'Delivery / Return Time']
    if not all(col in data_file.columns for col in required_columns):
        print(f"Missing required columns: {required_columns}")
        sys.exit(1)

    data_file['Courier Name'] = data_file['Courier Name'].str.strip()
    data_file['Status'] = data_file['Status'].str.strip().str.title()
    data_file['Delivery / Return Time'] = pd.to_datetime(data_file['Delivery / Return Time']).dt.date

    # Filter only Delivered and Picked
    filtered_df = data_file[data_file['Status'].isin(['Delivered', 'Picked'])]

    # Group and count orders
    summary = (
        filtered_df
        .groupby(['Courier Name', 'Delivery / Return Time', 'Status'])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Ensure both columns exist
    for col in ['Delivered', 'Picked']:
        if col not in summary.columns:
            summary[col] = 0

    # Calculate payment
    def calculate_payment(row):
        delivered = row['Delivered']
        picked = row['Picked']

        if delivered <= 20:
            delivered_payment = delivered * 12
        else:
            delivered_payment = (20 * 12) + ((delivered - 20) * 24)

        picked_payment = picked * 12
        return delivered_payment + picked_payment

    summary['Payment'] = summary.apply(calculate_payment, axis=1)

    # Output
    summary.to_csv("courier_payment_summary.csv", index=False)
    print(summary)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("No File Provided!")
