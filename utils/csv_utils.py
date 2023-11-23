import pandas as pd

def read_csv(filename, is_df=False):
    try:
        df = pd.read_csv(filename)
        if is_df:
            return df
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
    except pd.errors.EmptyDataError:
        print("No data: The file is empty.")
    except pd.errors.ParserError:
        print("Error during parsing the CSV file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def add_row_to_csv(filename, new_row):
    try:
        df = pd.read_csv(filename, index_col=0)
        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_row_df], ignore_index=True)
        df.to_csv(filename)
    except Exception as e:
        print(f"Error occurred: {e}")

def delete_row_from_csv_by_index(filename, index):
    try:
        df = pd.read_csv(filename, index_col=0)
        if index in df.index:
            df = df.drop(index, axis=0)
            df.to_csv(filename)
        else:
            print(f"No row found at index {index}")
    except Exception as e:
        print(f"Error occurred: {e}")

def modify_row_in_csv_by_index(filename, index, new_data):
    try:
        df = pd.read_csv(filename, index_col=0)
        if index in df.index:
            df.loc[index] = new_data
            df.to_csv(filename)
        else:
            print(f"No row found at index {index}")
    except Exception as e:
        print(f"Error occurred: {e}")
