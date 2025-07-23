import pandas as pd
import sys

if len(sys.argv) > 1:
    file_path = sys.argv[1]

    data_file = pd.read_csv(file_path)
    data_file.columns = data_file.columns.str.strip()
    delivered_picked_filter = data_file[data_file['Status'].isin(
        ['Delivered', 'Picked'])]

    grouping = delivered_picked_filter.groupby(
        ['Courier Name', 'Status']).size().unstack(fill_value=0).reset_index()

    if 'Delivered' not in grouping.columns:
        grouping['Delivered'] = 0
    if 'Picked' not in grouping.columns:
        grouping['Picked'] = 0

    # grouping.to_csv("courier_summary.csv", index=False)

    print(grouping)
else:
    print("No File Provided!")
