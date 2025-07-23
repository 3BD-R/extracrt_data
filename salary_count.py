import pandas as pd
import sys

if len(sys.argv) > 1:
    file_path = sys.argv[1]
    data_file = pd.read_csv(file_path)
    data_file.columns = data_file.columns.str.strip()

    data_file['Status'] = data_file['Status'].str.strip().str.title()

    filtered_df = data_file[data_file['Status'].isin(['Delivered', 'Picked'])]

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
    summary.to_csv("summary.csv", index=False)
    print(summary)

else:
    print("NO FILE PROVIDED")
