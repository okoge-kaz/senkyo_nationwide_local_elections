import pandas as pd


def convert_to_excel_from_csv(csv_file_path: str, excel_file_path: str):
    df = pd.read_csv(csv_file_path)
    df.to_excel(excel_file_path)


def main():
    for path_index in range(1, 13):
        csv_file_path = f"out/{path_index}/2019_{path_index}.csv"
        excel_file_path = f"out/senkyo_nationwide_local_elections_{path_index}.xlsx"
        convert_to_excel_from_csv(csv_file_path, excel_file_path)


if __name__ == "__main__":
    main()
