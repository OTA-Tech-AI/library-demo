import pandas as pd

def read_csv(filename, is_df=False):
    try:
        df = pd.read_csv(filename, index_col=0, encoding='ISO-8859-1')
        df_reset = df.reset_index()
        if is_df:
            return df_reset
        return df_reset.to_dict(orient='records')
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

def delete_row_from_csv_by_index(filename, index, cols_names, cols_values):
    try:
        df = pd.read_csv(filename, index_col=0)

        if index in df.index and \
            all(df.at[index, col] == val for col, val in zip(cols_names, cols_values)):

            df = df.drop(index, axis=0)
            df.to_csv(filename)
            return True
        else:
            print(f"No row found at index {index}")
            return False
    except Exception as e:
        print(f"Error occurred: {e}")

def modify_row_in_csv_by_index(filename, index, cols_names, cols_values, new_data):
    try:
        df = pd.read_csv(filename, index_col=0)
        if index in df.index and \
            all(df.at[index, col] == val for col, val in zip(cols_names, cols_values)):

            df.loc[index] = new_data
            df.to_csv(filename)
            return True
        else:
            print(f"No row found at index {index}")
            return False
    except Exception as e:
        print(f"Error occurred: {e}")
