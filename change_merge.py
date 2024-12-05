import pandas as pd

def check_data(value):
    if value == "" or pd.isna(value):
        return 0
    return 1

def main():
    merge_data = pd.read_csv('merged_data/merged_data.csv')
    merge_data['Q1 Time'] = merge_data['Q1 Time'].apply(check_data)
    merge_data['Q2 Time'] = merge_data['Q2 Time'].apply(check_data)
    merge_data['Q3 Time'] = merge_data['Q3 Time'].apply(check_data)
    merge_data.to_csv('merged_data/changed_merged_data.csv', index=False)

main()
