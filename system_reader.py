import csv
from collections import deque

# CSV and Deque Method
class CSVLastRowExtractor:
    """
    A class used to extract last row from a CSV file using a deque.
    
    Methods
    -------
    _read_last_row(file_path)
        Reads the CSV file and returns the header and the last row.
    
    extract_last_rows(file_path, columns)
        Extracts the last row's values for the specified columns.
    """
    @classmethod
    def _read_file(cls, file_path):
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                if header is None:
                    raise ValueError(f"File {file_path} is empty or has no header.")
                last_row = deque(reader, maxlen=1)
                if not last_row:
                    raise ValueError(f"File {file_path} has no data rows.")
                return header, last_row.pop()
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        except csv.Error as e:
            raise ValueError(f"Error parsing CSV file {file_path}: {str(e)}")

    @classmethod
    def extract_last_rows(cls, file_path, columns):
        """
        Extracts the last row's values for the specified columns.
        
        Parameters
        ----------
        file_path : str
            The path to the CSV file.
        columns : list
            A list of column names to extract from the last row.
            
        Returns
        -------
        list
            A list of values from the specified columns in the last row.
        """
        if not columns or not isinstance(columns, list):
            raise ValueError("Columns must be a non-empty list.")
        
        header, last_row = cls._read_file(file_path)
    
        try:
            # Find the indices of the desired columns
            indices = [header.index(column) for column in columns]
            # return the desired columns
            return [last_row[index] for index in indices]
        
        except ValueError as e:
            missing = set(columns) - set(header)
            raise ValueError(f"Columns not found in CSV {file_path}: {missing}") from e

# For testing
if __name__ == "__main__":
    # Example usage (assuming a test CSV exists)
    try:
        result = CSVLastRowExtractor.extract_last_rows('system_transactions.csv', ['transaction_id', 'amount'])
        print(f"Extracted values: {result}")
    except Exception as e:
        print(f"Error: {e}")